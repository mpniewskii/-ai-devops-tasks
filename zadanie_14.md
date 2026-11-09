# Analiza logów systemowych Docker

## 1. Fragment logów

```log
May 19 10:15:32 server dockerd[1234]: time="2025-05-19T10:15:32.123456789Z" level=info msg="Container 78a2b3c4 health status changed from starting to healthy"
May 19 10:16:45 server dockerd[1234]: time="2025-05-19T10:16:45.987654321Z" level=info msg="Container 78a2b3c4 failed to connect to 172.17.0.3:5432: connection refused"
May 19 10:16:47 server dockerd[1234]: time="2025-05-19T10:16:47.246813579Z" level=warning msg="Container 78a2b3c4 health status changed from healthy to unhealthy"
```

## 2. Co się dzieje w tych logach?

1. **10:15:32** – Kontener o ID `78a2b3c4` przeszedł pomyślnie wstępny test stanu zdrowia (`health check`). Jego status zmienił się ze `starting` na `healthy`.
2. **10:16:45** – Kontener spróbował połączyć się z bazą danych PostgreSQL pod adresem IP `172.17.0.3` na porcie `5432`. Połączenie zostało odrzucone (`connection refused`).
3. **10:16:47** – Dwie sekundy po odrzuceniu połączenia nastąpiła kolejna weryfikacja stanu kontenera. Ze względu na brak łączności z bazą danych, kontener zmienił status z `healthy` na `unhealthy`.

## 3. Zidentyfikowane problemy

* **Błąd połączenia z bazą danych (`connection refused` na porcie 5432):**
  * Usługa PostgreSQL pod adresem `172.17.0.3` uległa awarii (została zatrzymana lub zrestartowana).
  * Kontener z bazą danych zmienił adres IP (np. po restarcie), jeśli nie użyto nazewnictwa sieciowego w Dockerze.
  * Usługa bazy danych jest przeciążona i nie przyjmuje nowych połączeń.
* **Zmiana statusu kontenera na `unhealthy`:**
  * Mechanizm `healthcheck` kontenera `78a2b3c4` poprawnie wykrył brak komunikacji ze swoją zależnością (baza danych) i oznaczył kontener jako niesprawny.
* **Podatność wynikająca z bezpośrednich adresów IP:**
  * Odwoływanie się do bazy danych po adresie IP kontenera (`172.17.0.3`) zamiast po nazwie serwisu (np. `db` w sieci Docker Compose) tworzy kruche powiązania, które łatwo ulegają awarii przy restarcie kontenerów.