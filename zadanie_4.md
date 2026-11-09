# Ćwiczenie: Wpływ przypisania roli (Persony) na jakość i szczegółowość odpowiedzi AI

## 1. Zwykłe pytanie (bez przypisania roli)

### Prompt:

> Jak rozwiązać problem z dużym zużyciem pamięci przez kontener Docker?

### Odpowiedź AI:

Aby rozwiązać problem z dużym zużyciem pamięci przez kontener Docker, możesz podjąć następujące kroki:

1. **Ustaw limity pamięci w Dockerze**
   Możesz ograniczyć maksymalną ilość pamięci RAM, jaką kontener może zużyć, używając flagi `--memory` podczas uruchamiania:
   ```bash
   docker run -m 512m moja-aplikacja
   ```

2. **Sprawdź zużycie pamięci**
   Użyj polecenia `docker stats`, aby na żywo monitorować, ile pamięci zużywają poszczególne kontenery.

3. **Zoptymalizuj kod i aplikację**
   Często problem leży w samej aplikacji (np. wycieki pamięci w Node.js, Pythonie czy Javie). Przeanalizuj logi i użyj narzędzi profilujących.

4. **Zmniejsz rozmiar obrazu bazowego**
   Wybierz lżejsze obrazy bazowe, np. oparte na `alpine`, co może zmniejszyć narzut pamięciowy całego środowiska.

5. **Restartuj kontenery**
   Jeżeli problem występuje sporadycznie, możesz skonfigurować politykę restartu lub używać narzędzi typu Docker Swarm / Kubernetes do automatycznego odświeżania kontenerów.

---

## 2. Pytanie z przypisaną rolą (Senior DevOps Engineer)

### Prompt:

> Jesteś doświadczonym DevOps Engineerem z 10-letnim doświadczeniem. Jak rozwiązać problem z dużym zużyciem pamięci przez kontener Docker?

### Odpowiedź AI:

Rozwiązywanie problemów z pamięcią (OOM / High Memory Usage) w środowisku kontenerowym wymaga systemowego podejścia – od diagnostyki i profilowania, po optymalizację runtime'u i konfiguracyjne mechanizmy obronne. Oto mój sprawdzony proces diagnostyczno-naprawczy:

### Krok 1: Precyzyjna diagnostyka i telemetria
* **Analiza bieżąca (`docker stats` & `cgroups`):** Sprawdź odczyty z `docker stats --no-stream`. Pamiętaj, że Docker bazuje na Linux Kernel Control Groups (`cgroups`). Aby sprawdzić dokładne metryki jądra:
  ```bash
  cat /sys/fs/cgroup/memory/memory.stat
  ```
* **Logi systemowe i OOM Killer:** Sprawdź, czy proces w kontenerze nie jest zabijany przez kernel z powodu braku pamięci (Exit code 137):
  ```bash
  dmesg -T | grep -i oom
  docker inspect <container_id> --format='{{.State.ExitCode}}'
  ```
* **Obserwowalność:** Zweryfikuj wykresy RSS (Resident Set Size) i cache w Prometheus/Grafana lub Datadog, aby ustalić, czy zużycie rośnie liniowo (wyciek pamięci), czy skokowo (np. przy konkretnym zapytaniu HTTP).

### Krok 2: Ograniczenie i obsługa zasobów (Resource Limits)
Nie pozwól, aby pojedynczy kontener doprowadził do awarii całego węzła (Node Crash):
* **Hard/Soft Limits w CLI:**
  ```bash
  docker run -d --name app \
    --memory="1g" \
    --memory-reservation="768m" \
    --memory-swap="1.5g" \
    my-image:v1
  ```
* **W `docker-compose.yml` (v3.8+):**
  ```yaml
  services:
    app:
      image: my-image:v1
      deploy:
        resources:
          limits:
            cpus: '1.0'
            memory: 1Gb
          reservations:
            cpus: '0.5'
            memory: 512Mb
  ```

### Krok 3: Optymalizacja na poziomie Runtime i Stosu Aplikacji
Często Docker jedynie eksponuje błędy samej aplikacji:
* **Środowiska uruchomieniowe (Java/JVM, Node.js):**
  * **Java:** Zdefiniuj odpowiednie parametry sterty (Heap Size), np. `-XX:MaxRAMPercentage=75.0` zamiast sztywnych wartości `-Xmx`, aby JVM respektował limity `cgroups`.
  * **Node.js:** Ustaw `--max-old-space-size=1024` dla V8 engine.
* **Alokatory pamięci:** Zamiana domyślnego alokatora `glibc malloc` na `jemalloc` lub `tcmalloc` w obrazach Linuxowych często redukuje fragmentację pamięci nawet o 20-30%.

### Krok 4: Architektura obrazu (Multi-Stage Builds)
* Stosuj **Multi-Stage Builds**, aby wyeliminować kompilatory, pliki nagłówkowe i zbędne zależności ze środowiska uruchomieniowego:
  ```dockerfile
  # Stage 1: Build
  FROM node:18-alpine AS builder
  WORKDIR /app
  COPY . .
  RUN npm ci && npm run build

  # Stage 2: Runner
  FROM node:18-alpine AS runner
  WORKDIR /app
  COPY --from=builder /app/dist ./dist
  COPY --from=builder /app/node_modules ./node_modules
  CMD ["node", "dist/main.js"]
  ```

---

## 3. Porównanie i obserwacje

| Kryterium | Zapytanie bez roli | Zapytanie z rolą (Senior DevOps) |
| :--- | :--- | :--- |
| **Poziom szczegółowości** | Podstawowy / Ogólny | Zaawansowany / Inżynieryjny |
| **Słownictwo i żargon** | Prosty język (`limity pamięci`, `restartuj`) | Specjalistyczny (`cgroups`, `OOM Killer`, `RSS`, `Exit Code 137`, `jemalloc`, `Multi-Stage Build`) |
| **Podejście do problemu** | Liniowa lista ogólnych porad | Ustrukturyzowany proces inżynieryjny (Diagnostyka -> Zasoby -> Runtime -> Architektura) |
| **Jakość kodu / Konfiguracji** | Podstawowa komenda `docker run -m` | Produkcyjne przykłady: `docker-compose` v3.8, zmienne JVM, konteneryzacja wieloetapowa |
| **Użyteczność produkcyjna** | Dobra dla początkujących | Gotowa do wdrożenia w środowisku firmowym/produkcyjnym |

### Wnioski:

1. **Kontekst zmienia jakość odpowiedzi:** Narzucenie roli ekspertowi (Persona Prompting) zmusza model AI do sięgnięcia po pojęcia z głębszych warstw wiedzy dziedzinowej.
2. **Techniczne podejście do przyczyny:** Zwykła odpowiedź sugeruje powierzchowne kroki (np. "zrestartuj kontener"), podczas gdy rola inżyniera DevOps kładzie nacisk na dokładną diagnostykę (`cgroups`, `dmesg`, `memory.stat`), aby znaleźć przyczynę źródłową (Root Cause Analysis).
3. **Praktyczne wzorce produkcyjne:** Dodanie roli skutkuje wygenerowaniem gotowych snippetów konfiguracji (`docker-compose`, opcje JVM/Node), które odpowiadają rzeczywistym standardom w branży IT.