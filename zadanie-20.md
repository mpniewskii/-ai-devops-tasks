# Walidacja adresu IPv4 za pomocą wyrażenia regularnego

## Zapytanie (Prompt)

> Trzebuję wyrażenia regularnego, które waliduje format adresu IPv4 (np. `192.168.1.1`).

## Prośba o wyjaśnienie

> Wyjaśnij, jak działa to wyrażenie regularne i przetestuj je na kilku przykładach (poprawnych i niepoprawnych).

## 1. Wyrażenie regularne

Funkcja wykorzystująca wyrażenie regularne znajduje się w pliku [ipv4-validator.js](./ipv4-validator.js).

```javascript
/^(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)$/
```

Wyrażenie sprawdza standardowy zapis IPv4 składający się z czterech oktetów od `0` do `255`, rozdzielonych kropkami. Nie akceptuje zer wiodących, na przykład `01.2.3.4`.

## 2. Wyjaśnienie działania

### Zakres pojedynczego oktetu

Fragment:

```text
25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d
```

opisuje dozwolone wartości pojedynczego oktetu:

* `25[0-5]` — wartości od `250` do `255`,
* `2[0-4]\d` — wartości od `200` do `249`,
* `1\d\d` — wartości od `100` do `199`,
* `[1-9]?\d` — wartości od `0` do `99`, bez zer wiodących.

### Pozostałe elementy wyrażenia

* `\.` — dosłowna kropka oddzielająca oktety. Kropka musi być poprzedzona ukośnikiem, ponieważ sama kropka w regexie oznacza dowolny znak.
* `(?: ... )` — grupa nieprzechwytująca, używana do grupowania fragmentów bez zapisywania ich jako osobnych wyników.
* `{3}` — wymaga dokładnie trzech pierwszych oktetów zakończonych kropką.
* `^` — oznacza początek tekstu.
* `$` — oznacza koniec tekstu.

Dzięki kotwicom `^` i `$` cały tekst musi być adresem IPv4. Dodatkowe znaki przed adresem lub po nim powodują odrzucenie wartości.

## 3. Funkcja JavaScript

```javascript
const ipv4Pattern = /^(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)$/;

/**
 * Sprawdza, czy podany tekst ma poprawny format adresu IPv4.
 *
 * @param {string} address - Adres IP do sprawdzenia.
 * @returns {boolean} `true`, jeśli adres jest poprawnym adresem IPv4.
 */
function isValidIPv4(address) {
  return typeof address === 'string' && ipv4Pattern.test(address);
}

module.exports = isValidIPv4;
```

Sprawdzenie `typeof address === 'string'` zabezpiecza funkcję przed otrzymaniem wartości innego typu, na przykład `null`, liczby lub tablicy.

## 4. Przykłady testów

| Adres | Oczekiwany wynik | Powód |
|---|---:|---|
| `192.168.1.1` | `true` | Poprawny adres IPv4 |
| `0.0.0.0` | `true` | Najniższa możliwa wartość każdego oktetu |
| `255.255.255.255` | `true` | Najwyższa możliwa wartość każdego oktetu |
| `10.0.0.25` | `true` | Poprawny adres prywatny |
| `256.1.1.1` | `false` | Pierwszy oktet przekracza `255` |
| `192.168.1` | `false` | Brakuje jednego oktetu |
| `192.168.1.1.5` | `false` | Adres zawiera pięć oktetów |
| `192.168.01.1` | `false` | Oktet zawiera zero wiodące |
| `192.168.1.-1` | `false` | Oktet zawiera niedozwolony znak `-` |
| `192.168.1.1 ` | `false` | Dodatkowa spacja na końcu |

Przykładowy kod testujący:

```javascript
const isValidIPv4 = require('./ipv4-validator');

const addresses = [
  '192.168.1.1',
  '0.0.0.0',
  '255.255.255.255',
  '256.1.1.1',
  '192.168.1',
  '192.168.01.1'
];

addresses.forEach(address => {
  console.log(`${address}: ${isValidIPv4(address)}`);
});
```

Oczekiwany wynik:

```text
192.168.1.1: true
0.0.0.0: true
255.255.255.255: true
256.1.1.1: false
192.168.1: false
192.168.01.1: false
```
