# Analiza i optymalizacja algorytmu znajdowania par

## Zapytanie (Prompt)

> Jaka jest złożoność czasowa i pamięciowa tego algorytmu? Czy można go zoptymalizować?

## 1. Oryginalny algorytm

Oryginalny algorytm znajduje się w pliku [find-pairs.js](./find-pairs.js).

```javascript
function findPairs(arr, targetSum) {
  const pairs = [];
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] + arr[j] === targetSum) {
        pairs.push([arr[i], arr[j]]);
      }
    }
  }
  return pairs;
}
```

## 2. Analiza złożoności oryginalnego rozwiązania

### Złożoność czasowa

Algorytm wykorzystuje dwie zagnieżdżone pętle. Dla każdego elementu `i` sprawdzane są wszystkie elementy znajdujące się za nim, dlatego wykonywanych jest około `n * (n - 1) / 2` porównań.

* **Złożoność czasowa: `O(n²)`**

W najgorszym przypadku każda para elementów musi zostać sprawdzona.

### Złożoność pamięciowa

Poza tablicą wynikową algorytm używa stałej liczby zmiennych pomocniczych.

* **Pamięć pomocnicza: `O(1)`**
* **Pamięć wynikowa: `O(p)`**, gdzie `p` oznacza liczbę znalezionych par

Jeśli uwzględnimy tablicę `pairs`, całkowite zużycie pamięci wynosi `O(p)`. W najgorszym przypadku liczba par może być kwadratowa względem liczby elementów, więc wynik może zająć `O(n²)` pamięci.

## 3. Zoptymalizowana wersja

Zoptymalizowany algorytm znajduje się w pliku [find-pairs-optimized.js](./find-pairs-optimized.js).

```javascript
function findPairs(arr, targetSum) {
  const pairs = [];
  const seenValues = new Map();

  for (const value of arr) {
    const complement = targetSum - value;
    const matchingValues = seenValues.get(complement) || 0;

    for (let i = 0; i < matchingValues; i++) {
      pairs.push([complement, value]);
    }

    seenValues.set(value, (seenValues.get(value) || 0) + 1);
  }

  return pairs;
}
```

## 4. Opis optymalizacji

Zamiast porównywać każdy element z każdym kolejnym elementem, algorytm przechowuje w `Map` liczbę wystąpień wartości już przetworzonych.

1. Dla bieżącej wartości obliczany jest brakujący składnik sumy:
   `complement = targetSum - value`.
2. `Map` sprawdza, ile razy brakujący składnik wystąpił wcześniej.
3. Dla każdego wcześniejszego wystąpienia tworzona jest para.
4. Bieżąca wartość zostaje dodana do mapy.

Przechowywanie liczby wystąpień pozwala poprawnie obsługiwać duplikaty. Na przykład dla tablicy `[3, 3, 3]` i sumy `6` wynik zawiera trzy pary.

Zoptymalizowana wersja może zwracać poprawne pary w innej kolejności niż oryginalna, ponieważ dodaje parę podczas przetwarzania jej drugiego elementu. Jeśli kolejność wyników jest wymagana przez aplikację, można ją dodatkowo uporządkować.

## 5. Złożoność zoptymalizowanego rozwiązania

### Złożoność czasowa

Jedno przejście po tablicy wykonuje operacje odczytu i zapisu w `Map`, które średnio zajmują `O(1)`. Dodatkowa pętla tworzy tylko pary należące do wyniku.

* **Czas wyszukiwania: `O(n)` średnio**
* **Czas wraz z tworzeniem wyniku: `O(n + p)`**, gdzie `p` oznacza liczbę zwróconych par

Nie można uzyskać mniej niż `O(p)`, ponieważ każdą znalezioną parę trzeba utworzyć i zapisać w wyniku.

### Złożoność pamięciowa

Mapa przechowuje różne wartości z tablicy:

* **Pamięć pomocnicza: `O(n)`**
* **Pamięć wynikowa: `O(p)`**
* **Łącznie: `O(n + p)`**

## 6. Porównanie rozwiązań

| Właściwość | Oryginalny algorytm | Zoptymalizowany algorytm |
|---|---:|---:|
| Czas wyszukiwania | `O(n²)` | `O(n)` średnio |
| Czas z zapisem wyników | `O(n²)` | `O(n + p)` |
| Pamięć pomocnicza | `O(1)` | `O(n)` |
| Obsługa duplikatów | Tak | Tak |

Optymalizacja wymienia część pamięci na znacznie krótszy czas wyszukiwania. Jest szczególnie korzystna dla dużych tablic, gdy liczba wynikowych par nie dominuje nad kosztem samego wyszukiwania.
