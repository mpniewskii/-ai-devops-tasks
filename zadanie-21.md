# Konwersja danych JSON do formatu CSV

## Przykładowe dane JSON

Plik z oryginalnymi danymi znajduje się tutaj: [users.json](./users.json).

```json
{
  "users": [
    {
      "id": 1,
      "name": "Jan Kowalski",
      "email": "jan@example.com",
      "roles": ["admin", "user"]
    },
    {
      "id": 2,
      "name": "Anna Nowak",
      "email": "anna@example.com",
      "roles": ["user"]
    }
  ]
}
```

## Zapytanie (Prompt)

> Przekształć te dane JSON do formatu CSV z kolumnami: `id`, `name`, `email`, `roles`.

## Wynik konwersji

Wygenerowany plik CSV znajduje się tutaj: [users.csv](./users.csv).

```csv
id,name,email,roles
1,"Jan Kowalski",jan@example.com,"admin;user"
2,"Anna Nowak",anna@example.com,user
```

## Opis procesu konwersji

1. Odczytano tablicę `users` z obiektu JSON.
2. Każdy element tablicy `users` przekształcono na jeden wiersz CSV.
3. Wartości `id`, `name`, `email` i `roles` zapisano w osobnych kolumnach.
4. Tablicę `roles` zamieniono na tekst, łącząc jej elementy średnikiem.
5. Wartości tekstowe zawierające spacje umieszczono w cudzysłowie zgodnie ze składnią CSV.

## Potencjalne wyzwania

### Reprezentacja tablicy `roles`

JSON pozwala przechowywać tablicę jako strukturę danych, natomiast CSV jest formatem płaskim. W tym przykładzie role zapisano w jednej komórce jako `admin;user`.

Takie rozwiązanie zachowuje jeden wiersz na użytkownika i jest łatwe do odczytania. Przy ponownym przetwarzaniu pliku trzeba jednak pamiętać, że średnik jest separatorem ról, a nie separatorem kolumn CSV.

Alternatywne rozwiązania to:

* zapisanie tablicy jako tekstu JSON, np. `["admin","user"]`,
* utworzenie osobnej kolumny dla każdej możliwej roli,
* utworzenie wielu wierszy dla jednego użytkownika — po jednym wierszu dla każdej roli.

### Znaki specjalne i cudzysłowy

Jeśli wartość zawiera przecinek, znak nowej linii lub cudzysłów, musi zostać ujęta w cudzysłowy. Wewnętrzny cudzysłów należy podwoić, np. `Jan ""Kowalski""`.

### Kodowanie znaków

Dane zawierające polskie znaki powinny być zapisane w kodowaniu UTF-8. Zapobiega to problemom z wyświetlaniem znaków takich jak `ą`, `ę` lub `ł` w programach otwierających plik CSV.

### Puste lub brakujące wartości

W praktycznych danych niektóre pola mogą być puste albo nie występować w każdym obiekcie. Podczas konwersji należy ustalić, czy takie wartości będą zapisywane jako puste komórki, czy jako określony tekst, np. `N/A`.
