# Jenkins Configuration as Code (JCasC)

## Zapytanie (Prompt)

> Wygeneruj szablon Jenkins Configuration as Code (JCasC) w formacie YAML, który konfiguruje:
> - podstawowe ustawienia Jenkins (liczba wykonawców, timeout),
> - globalny katalog narzędzi (Maven, Node.js, Docker),
> - podstawowe wtyczki,
> - przykładowe zadanie typu pipeline.

## 1. Plik konfiguracyjny

Szablon znajduje się w pliku [jenkins-casc.yaml](./jenkins-casc.yaml).

Plik zawiera:

* podstawowe ustawienia Jenkinsa, w tym dwóch wykonawców,
* lokalne konto administratora tworzone na podstawie zmiennych środowiskowych,
* globalne instalacje Maven, Node.js i Docker,
* definicję przykładowego zadania `example-pipeline`,
* limit czasu wykonania pipeline'u wynoszący 30 minut.

## 2. Wtyczki wymagane przez konfigurację

Przed zastosowaniem pliku należy zainstalować co najmniej następujące wtyczki:

| Wtyczka | Zastosowanie |
|---|---|
| `configuration-as-code` | Wczytywanie konfiguracji JCasC z YAML |
| `job-dsl` | Tworzenie zadania pipeline z sekcji `jobs` |
| `workflow-aggregator` | Obsługa deklaratywnych pipeline'ów |
| `git` | Integracja z repozytoriami Git |
| `credentials-binding` | Bezpieczne przekazywanie danych uwierzytelniających do zadań |
| `maven-plugin` | Konfiguracja narzędzi Maven |
| `nodejs` | Konfiguracja narzędzi Node.js |
| `docker-workflow` | Używanie Dockera w pipeline'ach |

W praktycznej instalacji wersje wtyczek powinny być przypięte do wersji zgodnych z używaną wersją Jenkinsa.

## 3. Jak działa konfiguracja

### Podstawowe ustawienia

Sekcja `jenkins` ustawia między innymi:

* `numExecutors: 2` — Jenkins może wykonywać dwa zadania równolegle na controllerze lub przypisanym agencie.
* `mode: NORMAL` — Jenkins może wykonywać zadania na dostępnych agentach.
* `quietPeriod: 5` — zadanie czeka pięć sekund przed rozpoczęciem, co pozwala połączyć szybkie, kolejne wywołania.
* `scmCheckoutRetryCount: 2` — checkout kodu może zostać ponowiony po niepowodzeniu.

Timeout jest ustawiony w przykładowym pipeline:

```groovy
options {
  timeout(time: 30, unit: 'MINUTES')
}
```

Oznacza to, że pojedyncze wykonanie pipeline'u zostanie przerwane po 30 minutach.

### Globalne narzędzia

Sekcja `tool` definiuje instalacje:

* Maven `3.9.9`,
* Node.js `22.14.0`,
* Docker oznaczony jako `latest`.

Jenkins może pobrać te narzędzia automatycznie, jeśli agent ma dostęp do sieci. W środowisku produkcyjnym warto przypinać konkretne wersje zamiast używać `latest`.

### Przykładowe zadanie

Sekcja `jobs` korzysta z Job DSL i tworzy zadanie `example-pipeline`. Pipeline zawiera etapy `Build` i `Test`, a także znaczniki czasu oraz limit czasu wykonania.

## 4. Instalacja Jenkinsa i wymaganych wtyczek

Najprostszy sposób uruchomienia testowego Jenkinsa to Docker:

```powershell
docker network create jenkins
docker volume create jenkins_home
docker run -d --name jenkins `
  --network jenkins `
  -p 8080:8080 `
  -p 50000:50000 `
  -v jenkins_home:/var/jenkins_home `
  jenkins/jenkins:lts-jdk17
```

Po uruchomieniu otwórz `http://localhost:8080`, odczytaj hasło początkowe z logów kontenera i przejdź przez kreator instalacji.

Następnie zainstaluj w Jenkinsie wtyczki:

1. Otwórz **Manage Jenkins → Plugins**.
2. Wyszukaj i zainstaluj `Configuration as Code`, `Job DSL`, `Pipeline`, `Git`, `Credentials Binding`, `Maven Integration`, `NodeJS` oraz `Docker Pipeline`.
3. Uruchom ponownie Jenkinsa, jeśli interfejs o to poprosi.

## 5. Uruchomienie z JCasC

Skopiuj plik YAML do katalogu dostępnego dla procesu Jenkins i ustaw zmienną `CASC_JENKINS_CONFIG`. Przykład dla kontenera Docker:

```powershell
docker cp .\jenkins-casc.yaml jenkins:/var/jenkins_home/jenkins-casc.yaml
docker restart jenkins
```

Samo skopiowanie pliku nie wystarczy, jeśli zmienna nie została ustawiona przy uruchamianiu kontenera. Przygotuj kontener z konfiguracją zamontowaną jako wolumen:

```powershell
docker run -d --name jenkins-casc `
  -p 8080:8080 `
  -p 50000:50000 `
  -v "${PWD}\jenkins-casc.yaml:/var/jenkins_home/jenkins-casc.yaml:ro" `
  -e CASC_JENKINS_CONFIG=/var/jenkins_home/jenkins-casc.yaml `
  -e JENKINS_ADMIN_ID=admin `
  -e JENKINS_ADMIN_PASSWORD=zmien-to-haslo `
  -e JENKINS_URL=http://localhost:8080/ `
  jenkins/jenkins:lts-jdk17
```

Przed użyciem w środowisku współdzielonym zastąp przykładowe hasło bezpieczną wartością i nie zapisuj go w repozytorium ani historii powłoki.

## 6. Weryfikacja konfiguracji

Po uruchomieniu:

1. Otwórz Jenkins pod adresem skonfigurowanym w `JENKINS_URL`.
2. Sprawdź **Manage Jenkins → System**, czy widoczne są dwa executory.
3. Sprawdź **Manage Jenkins → Tools**, czy dostępne są Maven, Node.js i Docker.
4. Na stronie głównej potwierdź utworzenie zadania `example-pipeline`.
5. Uruchom zadanie i sprawdź, czy etapy `Build` oraz `Test` kończą się powodzeniem.

Jeśli konfiguracja nie zostanie zastosowana, sprawdź logi kontenera:

```powershell
docker logs jenkins-casc
```

## 7. Ważne zasady bezpieczeństwa

* Nie przechowuj haseł, tokenów ani kluczy w pliku YAML.
* Używaj zmiennych środowiskowych lub Jenkins Credentials.
* W produkcji nie uruchamiaj zadań z nieograniczonymi uprawnieniami administratora.
* Przypinaj wersje obrazu i wtyczek, aby konfiguracja była powtarzalna.
