# Ćwiczenie: Porównanie wyników promptowania (Docker i Node.js)

---

## 1. Prosty, niestrukturyzowany prompt

### Prompt:
> dockerfile node

### Odpowiedź AI (Prosty prompt):

Oto prosty przykład pliku `Dockerfile` dla aplikacji w Node.js:

```dockerfile
# Użyj oficjalnego obrazu Node.js
FROM node:latest

# Ustaw katalog roboczy w kontenerze
WORKDIR /usr/src/app

# Skopiuj pliki zależności
COPY package*.json ./

# Zainstaluj zależności
RUN npm install

# Skopiuj pozostałe pliki aplikacji
COPY . .

# Wystaw port (domyślnie 8080)
EXPOSE 8080

# Uruchom aplikację
CMD [ "node", "index.js" ]
```

---

## 2. Ustrukturyzowany i precyzyjny prompt

### Prompt:
> Napisz prosty Dockerfile dla aplikacji Node.js, który:
> - używa Node 18 jako obrazu bazowego
> - kopiuje pliki package.json i package-lock.json
> - instaluje zależności
> - kopiuje resztę plików aplikacji
> - wystawia port 3000
> - uruchamia aplikację poleceniem "npm start"

### Odpowiedź AI (Ustrukturyzowany prompt):

Oto gotowy `Dockerfile` spełniający wszystkie podane wymagania:

```dockerfile
# 1. Użycie Node 18 jako obrazu bazowego
FROM node:18

# Utworzenie i ustawienie katalogu roboczego
WORKDIR /app

# 2. Kopiowanie plików package.json oraz package-lock.json
COPY package.json package-lock.json ./

# 3. Instalacja zależności
RUN npm install

# 4. Kopiowanie pozostałych plików aplikacji
COPY . .

# 5. Wystawienie portu 3000
EXPOSE 3000

# 6. Uruchomienie aplikacji poleceniem "npm start"
CMD ["npm", "start"]
```

---

## 3. Porównanie i wnioski

| Cecha | Niestrukturyzowany prompt (`dockerfile node`) | Ustrukturyzowany prompt |
| :--- | :--- | :--- |
| **Wersja obrazu** | Domyślnie użył tagu `latest`, co nie jest zalecane na produkcji ze względu na brak powtarzalności. | Użył dokładnie wskazanej wersji (`node:18`). |
| **Port** | Ustalił losowy/domyślny port (`8080`). | Użył wskazanego portu (`3000`). |
| **Komenda startowa** | Użył ogólnego `node index.js`. | Użył specyficznej dla projektu komendy `npm start`. |
| **Precyzja kopiowania** | Użył wzorca `package*.json ./`. | Przekazał jawnie `package.json package-lock.json ./`. |

### Wnioski:
1. **Precyzja wymagań:** Precyzyjnie sformułowany prompt eliminuję zgadywanie po stronie modelu AI. W przypadku prostego promptu model zastosował domyślne, ogólne wartości.
2. **Bezpieczeństwo i przewidywalność:** Określenie konkretnych wersji (np. `node:18`) w strukturze promptu pozwala uniknąć problemów z kompatybilnością w przyszłości.
3. **Czas pracy:** Dobrze ustrukturyzowany prompt generuje kod gotowy do użycia bez konieczności wprowadzania ręcznych poprawek po wygenerowaniu odpowiedzi przez AI.