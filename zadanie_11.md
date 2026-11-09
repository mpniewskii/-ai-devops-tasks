# Testy jednostkowe z użyciem Jest

## Czym jest Jest?

**Jest** to popularny framework do testowania kodu w języku JavaScript, stworzony i rozwijany przez firmę Meta (Facebook). Służy do pisania i automatycznego uruchamiania testów jednostkowych oraz integracyjnych. Charakteryzuje się prostą konfiguracją (*zero-config*), szybkością działania oraz wbudowanymi narzędziami do asercji, atrap (mocków) i mierzenia pokrycia kodu testami (*code coverage*).

---

## Podstawowa struktura plików w projekcie

```text
my-project/
├── package.json
├── sum.js
└── sum.test.js
```

---

## Instrukcja instalacji i uruchomienia

### 1. Inicjalizacja projektu Node.js (jeśli plik package.json nie istnieje)

Wpisz w terminalu:
```bash
npm init -y
```

### 2. Instalacja frameworka Jest

Zainstaluj Jest jako zależność deweloperską (*devDependencies*):
```bash
npm install --save-dev jest
```

### 3. Konfiguracja skryptu testowego w `package.json`

Otwórz plik `package.json` i upewnij się, że w sekcji `"scripts"` znajduje się komenda uruchamiająca Jest:

```json
{
  "name": "my-project",
  "version": "1.0.0",
  "scripts": {
    "test": "jest"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  }
}
```

### 4. Uruchomienie testów

Aby uruchomić testy w projekcie, wykonaj polecenie:
```bash
npm test
```

Jest automatycznie wyszuka wszystkie pliki zakończone rozszerzeniem `.test.js` lub `.spec.js` i przeprowadzi zdefiniowane w nich testy.