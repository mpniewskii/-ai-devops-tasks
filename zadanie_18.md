# Praktki Bezpieczeństwa Docker w Środowisku Produkcyjnym

## 1. 5 Kluczowych Praktyk Bezpieczeństwa

1. **Uruchamianie kontenerów jako użytkownik inny niż root (Non-root user)**
   Domyślnie kontenery uruchamiają się z uprawnieniami konta `root`. Jeśli napastnik przełamie izolację kontenera, uzyskuje pełny dostęp do systemu gospodarza (hosta). Używanie dedykowanego użytkownika bez uprawnień administracyjnych ogranicza promień rażenia (blast radius).

2. **Używanie minimalnych i zaufanych obrazów bazowych (Minimal Base Images)**
   Stosowanie obrazów takich jak Distroless lub Alpine minimalizuje powierzchnię ataku poprzez usunięcie zbędnych narzędzi (np. `curl`, `bash`, kompilatorów), które mogłyby zostać wykorzystane przez intruza.

3. **Skanowanie obrazów pod kątem podatności (Vulnerability Scanning)**
   Regularne skanowanie obrazów za pomocą narzędzi takich jak Trivy, Grype czy Docker Scout w potoku CI/CD pozwala wykryć i zaktualizować znane luki bezpieczeństwa (CVE) przed wdrożeniem na produkcję.

4. **Ustawienie systemu plików tylko do odczytu (Read-Only Root Filesystem)**
   Uruchamianie kontenera z montowaniem głównego systemu plików w trybie tylko do odczytu zapobiega modyfikacji kodu źródłowego oraz wgrywaniu złośliwych plików wykonywalnych podczas trwania sesji.

5. **Ograniczanie zasobów oraz uprawnień jądra (Resource Limits & Capabilities)**
   Limity pamięci RAM i CPU chronią przed atakami typu Denial of Service (DoS), a usuwanie zbędnych uprawnień jądra (`--cap-drop=ALL`) blokuje zaawansowane techniki eksploitacji.

---

## 2. Pytanie Uzupełniające: Implementacja Użytkownika Non-Root

### W pliku `Dockerfile`

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Utworzenie grupy i użytkownika bez uprawnień roota
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY package*.json ./
RUN npm ci --only=production

COPY . .

# Zmiana właściciela plików aplikacji
RUN chown -R appuser:appgroup /app

# Przełączenie na bezpiecznego użytkownika
USER appuser

EXPOSE 3000
CMD ["node", "server.js"]
```

### W pliku `docker-compose.yml`

```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"
    user: "10001:10001" # Określenie UID:GID użytkownika bez uprawnień root
    read_only: true     # Dodatkowa praktyka: system plików tylko do odczytu
    tmpfs:
      - /tmp            # Temp w pamięci RAM dla tymczasowych zapisów
```