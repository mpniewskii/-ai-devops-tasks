# Diagnostyka błędu Docker: "address already in use"

## Komunikat błędu

```text
ERROR: for app  Cannot start service app: driver failed programming external connectivity on endpoint app (172.18.0.2): Error starting userland proxy: listen tcp4 0.0.0.0:3000: bind: address already in use
```

## Co oznacza ten błąd?

Błąd oznacza, że Docker próbuje przypisać port **3000** na Twojej maszynie (host) do usługi `app` w kontenerze, ale **port 3000 jest już używany** przez inny proces lub inny uruchomiony wcześniej kontener. 

System operacyjny nie pozwala na to, aby dwa procesy nasłuchiwały na tym samym porcie sieciowym jednocześnie.

---

## Jak rozwiązać ten problem?

### Sposób 1: Znalezienie i zatrzymanie procesu używającego portu 3000

#### Na systemie Linux / macOS:

1. **Znajdź PID procesu** korzystającego z portu 3000:
   ```bash
   lsof -i :3000
   # lub
   netstat -tulnp | grep 3000
   ```

2. **Zakończ ten proces**:
   ```bash
   kill -9 <PID_PROCESU>
   ```

#### Na systemie Windows (PowerShell / CMD):

1. **Znajdź PID procesu**:
   ```cmd
   netstat -ano | findstr :3000
   ```

2. **Zakończ ten proces**:
   ```cmd
   taskkill /PID <PID_PROCESU> /F
   ```

---

### Sposób 2: Zatrzymanie działających kontenerów Docker

Często port jest zablokowany przez inny, wciąż działający kontener Dockera.

1. **Zatrzymaj wszystkie działające kontenery**:
   ```bash
   docker stop $(docker ps -q)
   ```

2. **Jeśli używasz `docker-compose`**, wyłącz usługi w bieżącym projekcie:
   ```bash
   docker-compose down
   ```

---

### Sposób 3: Zmiana portu w pliku konfiguracyjnym

Jeżeli port 3000 musi pozostać zajęty przez inną aplikację, zmień przekierowanie portów na wolny port (np. 3001) po stronie hosta.

* **W `docker-compose.yml`:**
  ```yaml
  ports:
    - "3001:3000"  # Zmień z "3000:3000" na "3001:3000"
  ```

* **W komendzie `docker run`:**
  ```bash
  docker run -p 3001:3000 nazwa-obrazu
  ```