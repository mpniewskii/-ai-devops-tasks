# Dokumentowanie kodu w JavaScript za pomocą JSDoc

## Co to jest JSDoc?

**JSDoc** to standard komentowania kodu w języku JavaScript. Pozwala na opisywanie funkcji, parametrów, zwracanych wartości oraz typów danych za pomocą specjalnych znaczników wewnątrz bloku komentarza `/** ... */`.

## Dlaczego warto używać JSDoc?

1. **Lepsza podpowiedź w IDE:** Środowiska deweloperskie (np. VS Code) automatycznie wyświetlają opisy i typy podczas wpisywania nazwy funkcji.
2. **Statyczna kontrola typów:** Umożliwia wykrywanie błędów typowania bez konieczności migracji całego projektu do TypeScriptu.
3. **Automatyczna generacja dokumentacji:** Narzędzia takie jak `jsdoc` potrafią wygenerować czytelną stronę HTML z dokumentacją API całego projektu.

## Użyte znaczniki w przykładzie

* `@param {typ} nazwa - opis`: Opisuje parametr wejściowy funkcji.
* `@returns {typ} opis`: Opisuje typ oraz znaczenie zwracanej wartości (np. `Promise<UserData|null>`).
* `@typedef {Object} Nazwa`: Definiuje własny typ struktury danych.
* `@property {typ} nazwa - opis`: Opisuje pole wewnątrz zdefiniowanego typu `@typedef`.