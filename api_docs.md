# Dokumentacja API: Pobieranie Listy Użytkowników

## Endpoint

`GET /api/users`

Pobiera stronicowaną listę użytkowników z możliwością filtrowania według roli.

---

## Parametry Zapytania (Query Parameters)

| Parametr | Typ | Wymagany | Domyślnie | Opis |
| :--- | :--- | :--- | :--- | :--- |
| `page` | `integer` | Nie | `1` | Numer żądanej strony (min. 1). |
| `limit` | `integer` | Nie | `10` | Liczba wyników na stronę (min. 1, max. 100). |
| `role` | `string` | Nie | *brak* | Filtr według roli (np. `admin`, `user`, `editor`). |

---

## Przykładowe Żądanie

```http
GET /api/users?page=1&limit=2&role=admin HTTP/1.1
Host: api.example.com
Accept: application/json
```

---

## Odpowiedź (Response)

### Kod 200 OK

```json
{
  "status": "success",
  "meta": {
    "page": 1,
    "limit": 2,
    "total_items": 15,
    "total_pages": 8
  },
  "data": [
    {
      "id": "usr_94a2b1",
      "name": "Jan Kowalski",
      "email": "jan.kowalski@example.com",
      "role": "admin",
      "created_at": "2025-01-15T10:30:00Z"
    },
    {
      "id": "usr_10c8e4",
      "name": "Anna Nowak",
      "email": "anna.nowak@example.com",
      "role": "admin",
      "created_at": "2025-02-01T14:20:00Z"
    }
  ]
}
```

### Kod 400 Bad Request (Nieprawidłowy parametr)

```json
{
  "status": "error",
  "message": "Parametr 'limit' nie może być większy niż 100."
}
```