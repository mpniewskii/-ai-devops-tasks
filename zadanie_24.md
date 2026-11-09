# Analiza Metryk Wydajnościowych Serwera API (Zadanie 24)

## 1. Surowe dane wydajnościowe (ostatnie 24h)

* **Średni czas odpowiedzi:** 230ms
* **95 percentyl czasu odpowiedzi (p95):** 450ms
* **99 percentyl czasu odpowiedzi (p99):** 1200ms (1.2s)
* **Liczba zapytań:** 15,000
* **Liczba błędów 5xx:** 120 (0.8% wszystkich zapytań)
* **Użycie CPU:** Średnio 45%, Max 80%
* **Użycie pamięci RAM:** Średnio 2.1 GB, Max 3.5 GB (z 4 GB dostępnych)

---

## 2. Interpretacja danych i zidentyfikowane problemy

### 🔴 Problem 1: Ryzyko OOM (Out of Memory) i wysokie zużycie RAM
Pamięć RAM osiąga szczytowo **3.5 GB z 4 GB dostępnych (87.5%)**. 
* Taki poziom zużycia pamięci stwarza bezpośrednie zagrożenie uruchomienia mechanizmu Linux Kernel **OOM Killer**, który może bez ostrzeżenia zabić proces serwera API przy nagłym skoku ruchu.
* Różnica między średnim (2.1 GB) a maksymalnym zużyciem wskazuje na potencjalne wycieki pamięci (*memory leaks*) lub alokację bardzo dużych obiektów w pamięci podczas przetwarzania konkretnych żądań.

### 🔴 Problem 2: Błędy serwera (5xx Error Rate)
Wystąpiło **120 błędów typu 5xx** (ok. 0.8% zapytań). 
* W środowiskach produkcyjnych akceptowalny wskaźnik błędów po stronie serwera wynosi zazwyczaj poniżej 0.1%. 
* Błędy 5xx korelują z brakiem zasobów (np. limitami połączeń do bazy danych, timeoutami) lub nieobsłużonymi wyjątkami pod dużym obciążeniem.

### ⚠️ Problem 3: Długi ogon opóźnień (High Tail Latency - p99)
Mimo że średni czas odpowiedzi (230ms) i p95 (450ms) są akceptowalne, to **1% najwolniejszych zapytań (p99) trwa ponad 1.2 sekundy**.
* Wynika to z blokowania pętli zdarzeń, długich zapytań do bazy danych, przestojów na zbieranie śmieci (Garbage Collection spikes) lub rywalizacji o zasoby w momentach obciążenia CPU (peak 80%).

---

## 3. Sugestie i rekomendacje optymalizacyjne

1. **Zwiększenie zasobów / Skalowanie (Short-term fix):**
   * Zwiększ limit pamięci RAM dla serwera/kontenera z **4 GB do min. 6 GB - 8 GB**, aby zapobiec awarii OOM.
   * Rozważ skalowanie horyzontalne (dodanie drugiej instancji API za Load Balancerem), co odciąży CPU i zredukuje pik sygnałów p99.

2. **Profilowanie i analiza pamięci:**
   * Przeprowadź profilowanie alokacji pamięci (heap dump analysis), aby sprawdzić, co wywołuje skoki do 3.5 GB.
   * Upewnij się, że duże pliki/odpowiedzi są przesyłane strumieniowo (`streams`), a nie ładowane w całości do pamięci RAM.

3. **Optymalizacja zapytań i bazy danych:**
   * Przeanalizuj logi powolnych zapytań (Slow Query Logs) pod kątem braku indeksów w bazie danych, co bezpośrednio skraca czas p99.

4. **Obsługa błędów i telemetria:**
   * Wdróż narzędzie APM (np. Sentry, Datadog), aby zidentyfikować dokładne adresy URL i wyjątki wywołujące 120 błędów 5xx.