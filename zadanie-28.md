# Zarządzanie Jenkins przez API w Pythonie

## Zapytanie (Prompt)

> Napisz skrypt w Pythonie, który używa Jenkins API do:
> - listowania wszystkich zadań (jobs),
> - sprawdzania statusu ostatnich buildów,
> - uruchamiania wybranego zadania.
>
> Uwzględnij obsługę autoryzacji i obsługę błędów.

## 1. Skrypt

Skrypt znajduje się w pliku [jenkins-manager.py](./jenkins-manager.py).

Program udostępnia dwa polecenia:

* `list` — pobiera z Jenkinsa wszystkie zadania i wyświetla status oraz numer ostatniego builda.
* `run JOB_NAME` — uruchamia wybrane zadanie i wyświetla adres wpisu w kolejce Jenkins.

## 2. Użyte biblioteki

Skrypt korzysta wyłącznie ze standardowej biblioteki Pythona:

* `argparse` — obsługuje argumenty wiersza poleceń.
* `urllib.request` — wysyła żądania HTTP do Jenkins API oraz obsługuje uwierzytelnianie Basic Auth.
* `urllib.error` — pozwala obsłużyć błędy HTTP i problemy z połączeniem.
* `urllib.parse` — bezpiecznie buduje adresy URL i koduje nazwy zadań.
* `json` — odczytuje odpowiedzi JSON z API Jenkinsa.
* `os` — odczytuje dane dostępowe ze zmiennych środowiskowych.

Nie jest wymagana instalacja pakietu `python-jenkins` ani `requests`.

## 3. Autoryzacja

Jenkins powinien być skonfigurowany z użytkownikiem i tokenem API. Token jest bezpieczniejszy niż używanie hasła w skrypcie.

Dane dostępowe można przekazać przez zmienne środowiskowe:

```powershell
$env:JENKINS_URL = "http://localhost:8080"
$env:JENKINS_USER = "admin"
$env:JENKINS_API_TOKEN = "token-uzytkownika"
```

Można też przekazać je jako argumenty:

```powershell
python .\jenkins-manager.py --url http://localhost:8080 --username admin --api-token token-uzytkownika list
```

Token nie powinien być zapisywany bezpośrednio w repozytorium ani przekazywany w dokumentacji projektu.

## 4. Przykładowe użycie

### Listowanie zadań i statusów

```powershell
python .\jenkins-manager.py list
```

Przykładowy wynik:

```text
backend-build | status: SUCCESS | ostatni build: 42
frontend-tests | status: FAILURE | ostatni build: 18
```

Jeśli zadanie nie ma jeszcze builda, program wyświetli `brak`. Gdy Jenkins nie udostępnia wyniku, używany jest jego kolor statusu, na przykład `blue` lub `red`.

### Uruchamianie zadania

```powershell
python .\jenkins-manager.py run backend-build
```

Dla zadania w folderze:

```powershell
python .\jenkins-manager.py run "deploy/production"
```

Jenkins zwraca wtedy adres elementu kolejki. Skrypt używa tego adresu do poinformowania, że żądanie uruchomienia zostało przyjęte.

## 5. Jak działa skrypt

1. Argumenty CLI są odczytywane przez `argparse`.
2. `JenkinsClient` tworzy klienta HTTP z uwierzytelnianiem Basic Auth, używając nazwy użytkownika i tokena API.
3. Polecenie `list` wysyła żądanie do `api/json` z parametrem `tree`, aby pobrać nazwy zadań oraz dane ostatnich buildów.
4. Polecenie `run` pobiera CSRF crumb z `crumbIssuer/api/json`.
5. Następnie wysyłane jest żądanie `POST` do `job/<nazwa>/build` z nagłówkiem crumb.
6. Nazwy zadań zawierające foldery są kodowane bezpiecznie w adresie URL.

## 6. Obsługa błędów

Własny wyjątek `JenkinsApiError` pozwala przekazywać czytelne komunikaty w przypadku:

* braku adresu Jenkinsa lub danych autoryzacyjnych,
* błędów HTTP, takich jak `401`, `403` lub `404`,
* niedostępnego serwera Jenkins,
* niepoprawnej odpowiedzi JSON,
* braku lub niepoprawnej odpowiedzi CSRF crumb.

Skrypt kończy działanie kodem `0` po sukcesie, kodem `1` po błędzie API lub połączenia oraz kodem `2`, gdy nie podano wymaganych danych CLI.
