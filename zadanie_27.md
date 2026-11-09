# Zależności i sekwencja etapów w pipeline CI/CD Jenkins (Zadanie 27)

## 1. Wyjaśnienie zależności między etapami

W zaprojektowanym potoku CI/CD każdy krok bazuje na poprawnym wykonaniu poprzedniego (kaskadowa walidacja):

1. **Checkout Kodu $\rightarrow$ Budowanie Aplikacji:** 
   Pipeline musi w pierwszej kolejności pobrać najnowszą wersję kodu z repozytorium (np. Git), aby móc rozpocząć proces kompilacji lub przygotowania pakietu wykonawczego.

2. **Budowanie $\rightarrow$ Testy Jednostkowe:**
   Testy jednostkowe mogą zostać uruchomione dopiero wtedy, gdy kod bezbłędnie się buduje i wszystkie zależności zostały prawidłowo rozwiązane.

3. **Testy Jednostkowe $\rightarrow$ Analiza Statyczna (SonarQube) & Bezpieczeństwo:**
   Przejście testów funkcjonalnych na poziomie jednostkowym pozwala na rozpoczęcie analizy jakościowej (np. badanie *code coverage*, wykrywanie *code smells*) oraz skanowania pod kątem znanych podatności (SAST / skanowanie zależności).

4. **Analiza & Bezpieczeństwo $\rightarrow$ Budowanie Obrazu Docker:**
   Obraz kontenera jest tworzony tylko wtedy, gdy kod spełnia kryteria jakościowe oraz bezpieczeństwa (*Quality Gate*). Zapobiega to marnowaniu zasobów rejestru na obrazy zawierające luki lub błędy.

5. **Obraz Docker $\rightarrow$ Testy Integracyjne:**
   Po zbudowaniu kontenera uruchamia się środowisko testowe, na którym sprawdzana jest komunikacja aplikacji z zewnętrznymi usługami (np. bazą danych).

6. **Testy Integracyjne $\rightarrow$ Staging $\rightarrow$ Produkcja:**
   Pozytywny wynik testów integracyjnych pozwala na automatyczne wdrożenie aplikacji na środowisko testowe (*Staging*). Wdrożenie na produkcję wymaga zazwyczaj zatwierdzenia manualnego (*Manual Gate / Approval*), co stanowi biznesowy bufor bezpieczeństwa.