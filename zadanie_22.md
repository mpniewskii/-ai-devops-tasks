# Simple Task API

REST API do zarządzania zadaniami, napisane w Node.js z wykorzystaniem Express oraz bazy danych MongoDB.

## Opis

Simple Task API to lekkie rozwiązanie pozwalające na pełne zarządzanie cyklem życia zadań (CRUD). Aplikacja oferuje wbudowany system autoryzacji użytkowników oraz mechanizmy filtrowania listy zadań według ich statusu oraz priorytetu.

### Główne funkcje:
- **Zarządzanie zadaniami:** Tworzenie, odczytywanie, edycja oraz usuwanie zadań (CRUD).
- **Filtrowanie:** Wyszukiwanie zadań wg statusu oraz priorytetu.
- **Autoryzacja:** Prosty system rejestracji i logowania użytkowników.

## Instalacja

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/mpniewskii/-ai-devops-tasks.git
   cd simple-task-api
   ```

2. Zainstaluj zależności:
   ```bash
   npm install
   ```

3. Skonfiguruj zmienne środowiskowe w pliku `.env`:
   ```env
   PORT=3000
   MONGO_URI=mongodb://localhost:27017/tasks
   JWT_SECRET=super_secret_key
   ```

## Użycie

Uruchomienie serwera w trybie produkcyjnym:
```bash
npm start
```

Uruchomienie w trybie deweloperskim:
```bash
npm run dev
```

Serwer domyślnie działa pod adresem `http://localhost:3000`.

## Endpointy API

### Autoryzacja
- `POST /api/auth/register` - Rejestracja nowego użytkownika
- `POST /api/auth/login` - Logowanie użytkownika

### Zadania
- `GET /api/tasks` - Pobranie listy zadań (opcjonalne parametry query: `status`, `priority`)
- `GET /api/tasks/:id` - Pobranie szczegółów danego zadania
- `POST /api/tasks` - Utworzenie nowego zadania
- `PUT /api/tasks/:id` - Aktualizacja zadania
- `DELETE /api/tasks/:id` - Usuwanie zadania