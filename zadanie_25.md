# Wyjaśnienie etapów Jenkinsfile i najlepsze praktyki

## 1. Wyjaśnienie krok po kroku

### Konfiguracja wstępna (`agent` & `environment`)
* **`agent any`**: Wskazuje Jenkinsowi, że ten pipeline może wykonać się na dowolnym dostępnym węźle (node/agent).
* **`environment`**: Zdefiniowane tu zmienne są dostępne w całym procesie. Przechowują m.in. nazwę obrazu, tag (bazujący na unikalnym numerze budowania `${BUILD_NUMBER}`) oraz identyfikator poświadczeń z magazynu Jenkinsa.

### Etapy (`stages`)

1. **Stage: Checkout**
   * Pobiera najnowszą wersję kodu źródłowego z repozytorium Git powiązanego z danym zadaniem w Jenkinsie.

2. **Stage: Install Dependencies**
   * Wykonuje polecenie `npm ci` (zweryfikowana instalacja z `package-lock.json`), aby odtworzyć dokładnie takie same wersje pakietów jak w środowisku lokalnym.

3. **Stage: Run Tests**
   * Uruchamia zestaw testów automatycznych (`npm test`). Zapewnia to, że kod spełnia kryteria jakościowe i nie zawiera regresji.

4. **Stage: Build App**
   * Kompiluje i przygotowuje pliki produkcyjne aplikacji (`npm run build`), np. bundle JavaScript czy assets.

5. **Stage: Build Docker Image**
   * Tworzy obraz kontenera Docker za pomocą `docker build`, nadając mu unikalny tag odpowiadający numerowi budowania Jenkinsa.

6. **Stage: Push Docker Image**
   * Bezpiecznie loguje się do rejestru kontenerów za pomocą zapisanych w Jenkinsie poświadczeń (`REGISTRY_CREDENTIALS`) i wysyła gotowy obraz Docker na serwer zewnętrzny (np. Docker Hub, ECR, GAR).

### Bloki czyszczące (`post`)
* **`always { cleanWs() }`**: Czyści obszar roboczy (`workspace`) po zakończeniu potoku (niezależnie od wyniku), zapobiegając przepełnieniu dysku.

---

## 2. Najlepsze praktyki przy tworzeniu pipeline'ów Jenkins

1. **Składnia deklaratywna:** Zawsze preferuj deklaratywny Jenkinsfile (`pipeline { ... }`) nad skryptowym (`node { ... }`), ze względu na czytelność, walidację i łatwiejszą obsługę błędów.
2. **Używanie `npm ci` zamiast `npm install`:** Zapewnia deterministyczne budowanie aplikacji dzięki rygorystycznemu trzymaniu się wersji zapisanych w `package-lock.json`.
3. **Zarządzanie sekretami:** Nigdy nie wpisuj haseł ani tokenów bezpośrednio w pliku Jenkinsfile. Używaj mechanizmu *Jenkins Credentials* oraz bloku `withCredentials` lub `docker.withRegistry()`.
4. **Dynamiczne i unikalne tagowanie obrazów:** Zamiast używać tagu `:latest`, taguj obrazy unikalnymi identyfikatorami (np. `${BUILD_NUMBER}` lub HASH commitu z Gita), co umożliwia łatwe cofanie zmian (*rollback*).
5. **Czyszczenie obszaru roboczego:** Regularnie czyść `workspace` za pomocą `cleanWs()` w sekcji `post`, aby unikać problemów z brakiem miejsca na dysku agenta.