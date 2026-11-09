# Analiza i poprawa składni pliku Docker Compose YAML

## 1. Oryginalny (błędny) plik YAML

```yaml
 services:
  web:
    image: nginx
    ports:
- "80:80"
  app:
    build: .
    ports
- "3000:3000"
    depends_on:
- db
  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD=password
```

## 2. Znalezione błędy

1. **Niewłaściwa spacja na samym początku (spacja wcięciowa przed `services:`):**
   * Plik zaczyna się od spacji przed kluczem `services`, co powoduje błąd składniowy klucza najwyższego poziomu.

2. **Niepoprawne wcięcia elementów list (`ports`, `depends_on`):**
   * Elementy list zaczynające się od `-` (np. `- "80:80"`, `- "3000:3000"`, `- db`) zostały umieszczone bez żadnych wcięć od lewej krawędzi, zamiast być wcięte względem swoich sekcji nadrzędnych.

3. **Brak dwukropka (`:`) po kluczu `ports`:**
   * W sekcji serwisu `app` wpisano `ports` zamiast `ports:`.

4. **Niepoprawny zapis zmiennej środowiskowej w sekcji `environment`:**
   * Użyto zapisu w stylu pliku `.env` (`POSTGRES_PASSWORD=password`) zamiast prawidłowej składni mapy YAML (`POSTGRES_PASSWORD: password`) lub listy (`- POSTGRES_PASSWORD=password`).

## 3. Poprawiona wersja YAML

```yaml
services:
  web:
    image: nginx
    ports:
      - "80:80"

  app:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - db

  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD: password
```