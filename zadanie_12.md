# Optymalizacja funkcji znajdowania duplikatów w Pythonie

## Zapytanie (Prompt)

> Czy ten kod można zoptymalizować? Jeśli tak, zaproponuj bardziej wydajną wersję.

---

## 1. Oryginalna wersja kodu

```python
def find_duplicates(list_of_items):
    duplicates = []
    for i in range(len(list_of_items)):
        for j in range(i+1, len(list_of_items)):
            if list_of_items[i] == list_of_items[j] and list_of_items[i] not in duplicates:
                duplicates.append(list_of_items[i])
    return duplicates
```

### Problemy wydajnościowe oryginalnej wersji:

1. **Złożoność czasowa $O(n^2)$:** Zastosowanie dwóch zagnieżdżonych pętli `for` sprawia, że liczba porównań rośnie kwadratowo wraz ze wzrostem długości listy.
2. **Liniowe wyszukiwanie w liście:** Warunek `list_of_items[i] not in duplicates` przeszukuje całą listę `duplicates` element po elemencie, co w najgorszym scenariuszu dodatkowo narzuca operację $O(n)$, prowadząc do złożoności bliskiej $O(n^3)$.

---

## 2. Zoptymalizowana wersja kodu

```python
def find_duplicates(list_of_items):
    seen = set()
    duplicates = set()
    
    for item in list_of_items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
            
    return list(duplicates)
```

---

## 3. Wyjaśnienie usprawnień

* **Redukcja złożoności czasowej do $O(n)$:** Dzięki zastosowaniu zbiorów (`set`), sprawdzenie obecności (`item in seen`) oraz dodawanie elementu (`seen.add()`) odbywają się w czasie stałym $O(1)$. Pętla przechodzi przez listę tylko raz.
* **Brak zbędnych porównań:** Nie ma potrzeby sprawdzania par elementów ani używania indeksów `i` oraz `j`.
* **Zwięzłość i czytelność:** Kod jest prostszy, bardziej idiomatyczny dla języka Python (tzw. *pythonic*) i mniej podatny na błędy brzegowe.