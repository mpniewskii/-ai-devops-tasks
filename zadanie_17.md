# Filtrowanie i transformacja zadań w JavaScript

## Opis rozwiązania

Funkcja `getCompletedTaskTitles` przetwarza wejściową tablicę obiektów zadań w trzech krokach z wykorzystaniem wbudowanych metod tablicowych JavaScript (`chaining`):

1. **`filter(task => task.status === 'completed')`** – odrzuca wszystkie zadania, których status jest inny niż `"completed"`.
2. **`sort((a, b) => a.id - b.id)`** – sortuje przefiltrowane zadania rosnąco według numerycznego identyfikatora `id`.
3. **`map(task => task.title)`** – wyciąga z każdego obiektu wyłącznie pole `title`, zwracając tablicę łańcuchów znaków (stringów).

---

## Przykład użycia

```javascript
const getCompletedTaskTitles = require('./task-filter');

const tasks = [
  { id: 3, title: 'Wdrożenie na produkcję', status: 'completed' },
  { id: 1, title: 'Przygotowanie środowiska', status: 'completed' },
  { id: 4, title: 'Pisanie testów', status: 'in_progress' },
  { id: 2, title: 'Konfiguracja CI/CD', status: 'completed' },
  { id: 5, title: 'Przegląd kodu', status: 'pending' }
];

const completedTitles = getCompletedTaskTitles(tasks);
console.log(completedTitles);
// Wynik w konsoli:
// [ 'Przygotowanie środowiska', 'Konfiguracja CI/CD', 'Wdrożenie na produkcję' ]
```