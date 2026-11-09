# Dlaczego ważne jest ignorowanie wskazanych plików w .gitignore?

Plik `.gitignore` zapobiega śledzeniu i wysyłaniu niepotrzebnych lub wrażliwych plików do repozytorium Git. Oto kluczowe powody dla poszczególnych kategorii:

## 1. Bezpieczeństwo (Zmienne środowiskowe i sekrety)
* **Pliki `.env`**: Przechowują klucze API, hasła do baz danych, tokeny autoryzacyjne i parametry konfiguracyjne. Wyciek pliku `.env` do publicznego repozytorium jest jedną z najczęstszych przyczyn naruszenia bezpieczeństwa systemów.

## 2. Rozmiar repozytorium i wydajność
* **Folder `node_modules/`**: Zawiera tysiące zainstalowanych bibliotek, z których składają się zależności aplikacji. Modyfikacje w tym folderze generują ogromną liczbę niepotrzebnych commitów. Zależności powinny być pobierane automatycznie poleceniem `npm install` na podstawie plików `package.json` i `package-lock.json`.
* **Dane bazy danych (`mongo-data/`, `data/db/`)**: Wolumeny lokalne MongoDB oraz pliki bazy danych mogą ważyć od kilkudziesięciu megabajtów do wielu gigabajtów.

## 3. Izolacja środowiska deweloperskiego i lokalnych danych
* **Baza danych MongoDB**: Dane lokalne są unikalne dla komputera konkretnego programisty. Wysyłanie ich do repozytorium nadpisywałoby dane innych członków zespołu i prowadziło do konfliktów.

## 4. Spójność budowania kodu (Build Artifacts)
* **Foldery `dist/`, `build/`**: Pliki wynikowe kompilacji/transpilacji są generowane automatycznie podczas procesu produkcyjnego lub CI/CD. Repozytorium powinno przechowywać kod źródłowy, a nie skompilowane artefakty.

## 5. Unikanie konfliktów systemowych i edytorów
* **Pliki systemowe i IDE (`.DS_Store`, `.vscode/`, `.idea/`)**: Każdy system (macOS, Windows) i edytor (VS Code, WebStorm) tworzy własne ukryte pliki konfiguracyjne. Wrzucenie ich do repozytorium powoduje zbędny hałas w historii Git i może uniemożliwić innym wygodną pracę na odmiennych konfiguracjach.