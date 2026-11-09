# Diagram ASCII Art: Przepływ danych w aplikacji

## 1. Prosty diagram ASCII Art

### Prompt:
> Stwórz prosty diagram ASCII Art przedstawiający połączenie klienta, serwera aplikacji i bazy danych.

### Wygenerowany diagram:

```text
[ Klient ] <---> [ Serwer Aplikacji ] <---> [ Baza Danych ]
```

---

## 2. Ulepszony diagram z opisami i kierunkami przepływu

### Prompt:
> Dodaj do diagramu opisy elementów i kierunki przepływu danych.

### Wygenerowany diagram:

```text
+-----------------------+
|  Klient (Przeglądarka) |
+-----------------------+
       |         ^
       | Żądanie | Odpowiedź
       | (HTTP)  | (JSON/HTML)
       v         |
+-----------------------+
|   Serwer Aplikacji    | (Processing / Biznesowa logika)
+-----------------------+
       |         ^
       | Zapytanie| Dane
       | (SQL)   | (Wynik)
       v         |
+-----------------------+
|      Baza Danych      | (Przechowywanie danych)
+-----------------------+
```