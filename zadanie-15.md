# Refaktoryzacja funkcji konfiguracji środowiska

## Zapytanie (Prompt)

> Zrefaktoryzuj tę funkcję, aby była bardziej czytelna i łatwiejsza w utrzymaniu.

## 1. Oryginalna wersja kodu

Oryginalna funkcja znajduje się w pliku [config.js](./config.js).

```javascript
function getEnvironmentConfig(env) {
  if (env === 'development') {
    return {
      apiUrl: 'http://localhost:3000/api',
      debug: true,
      timeout: 5000
    };
  } else if (env === 'testing') {
    return {
      apiUrl: 'http://test-server:3000/api',
      debug: true,
      timeout: 5000
    };
  } else if (env === 'staging') {
    return {
      apiUrl: 'https://staging.example.com/api',
      debug: false,
      timeout: 10000
    };
  } else if (env === 'production') {
    return {
      apiUrl: 'https://api.example.com',
      debug: false,
      timeout: 15000
    };
  } else {
    return {
      apiUrl: 'http://localhost:3000/api',
      debug: true,
      timeout: 5000
    };
  }
}
```

### Problemy w oryginalnej wersji

1. **Długi łańcuch `if/else`:** Każde kolejne środowisko wymaga dodania następnego warunku.
2. **Powielona konfiguracja domyślna:** Konfiguracja dla środowiska `development` jest taka sama jak konfiguracja używana dla nieznanych wartości `env`.
3. **Trudniejsze utrzymanie:** Dane konfiguracyjne i logika wyboru są wymieszane w wielu instrukcjach warunkowych.

## 2. Zrefaktoryzowana wersja kodu

Zrefaktoryzowana funkcja znajduje się w pliku [config-refactored.js](./config-refactored.js).

```javascript
const defaultConfig = {
  apiUrl: 'http://localhost:3000/api',
  debug: true,
  timeout: 5000
};

const environmentConfigs = {
  development: defaultConfig,
  testing: {
    apiUrl: 'http://test-server:3000/api',
    debug: true,
    timeout: 5000
  },
  staging: {
    apiUrl: 'https://staging.example.com/api',
    debug: false,
    timeout: 10000
  },
  production: {
    apiUrl: 'https://api.example.com',
    debug: false,
    timeout: 15000
  }
};

function getEnvironmentConfig(env) {
  return environmentConfigs[env] || defaultConfig;
}
```

## 3. Opis zmian

* Zastąpiono łańcuch instrukcji `if/else` obiektem `environmentConfigs`, który przechowuje konfiguracje środowisk.
* Wydzielono konfigurację domyślną do zmiennej `defaultConfig`.
* Funkcja pobiera konfigurację bezpośrednio na podstawie nazwy środowiska.
* Dla nieznanego środowiska funkcja nadal zwraca konfigurację domyślną, tak jak w oryginalnej wersji.

## 4. Korzyści z refaktoryzacji

1. **Lepsza czytelność:** Dane konfiguracyjne są zebrane w jednym miejscu, a funkcja wyboru ma tylko jedną instrukcję.
2. **Łatwiejsze dodawanie środowisk:** Aby dodać nowe środowisko, wystarczy dopisać właściwość do obiektu `environmentConfigs`.
3. **Mniej powtórzeń:** Konfiguracja domyślna jest zdefiniowana tylko raz.
4. **Mniejsze ryzyko błędów:** Krótsza logika wyboru ogranicza liczbę warunków, które trzeba utrzymywać.
5. **Zachowanie dotychczasowego działania:** Obsługiwane środowiska zwracają te same wartości, a nieznane wartości nadal korzystają z konfiguracji lokalnej.
