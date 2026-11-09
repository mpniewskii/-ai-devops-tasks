# Naprawa błędów w Jenkinsfile

## Zapytanie (Prompt)

> Ten Jenkinsfile zawiera kilka błędów. Znajdź je i zaproponuj poprawioną wersję. Wyjaśnij, jakie były problemy i jak je naprawiłeś.

## 1. Jenkinsfile z błędami

Oryginalny plik znajduje się tutaj: [Jenkinsfile-with-errors](./Jenkinsfile-with-errors).

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            stesp {
                sh 'npm install'
                sh 'npm build'
            }
        }
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker build -t myapp .'
                sh 'docker push myapp:latest'
            }
            when {
                branch 'master'
            }
        }
    }
}
```

## 2. Poprawiona wersja

Poprawiony plik znajduje się tutaj: [Jenkinsfile-fixed](./Jenkinsfile-fixed).

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker build -t myapp:latest .'
                sh 'docker push myapp:latest'
            }
            when {
                branch 'master'
            }
        }
    }
}
```

## 3. Znalezione błędy i poprawki

### Błąd 1: Literówka `stesp`

W sekcji `Build` użyto:

```groovy
stesp {
```

W Jenkins Declarative Pipeline poprawnym blokiem jest `steps`. Literówka powoduje błąd składni i uniemożliwia uruchomienie pipeline'u.

Poprawiono na:

```groovy
steps {
```

### Błąd 2: Niepoprawna komenda budowania aplikacji

Użyto polecenia:

```bash
npm build
```

`npm` uruchamia skrypty zapisane w `package.json` za pomocą składni `npm run <nazwa>`. Dlatego poprawne polecenie to:

```bash
npm run build
```

### Błąd 3: Niejednoznaczny tag obrazu Docker

Obraz był budowany poleceniem:

```bash
docker build -t myapp .
```

a następnie wysyłany jako:

```bash
docker push myapp:latest
```

Docker domyślnie interpretuje `myapp` jako `myapp:latest`, więc w tym przypadku polecenia mogą działać. Dla większej czytelności i jednoznaczności tag `:latest` został jednak podany jawnie już podczas budowania:

```bash
docker build -t myapp:latest .
```

W ten sposób tag używany podczas budowania jest dokładnie taki sam jak tag przekazywany do `docker push`.

## 4. Elementy zachowane bez zmian

* `agent any` pozwala Jenkinsowi wybrać dowolnego dostępnego agenta.
* Etapy są wykonywane w kolejności: `Build`, `Test`, a następnie `Deploy`.
* Testy są uruchamiane poleceniem `npm test`.
* Deploy uruchamia się tylko dla gałęzi `master` dzięki warunkowi `when`.

Warunek `branch 'master'` jest typowym rozwiązaniem dla pipeline'u uruchamianego w kontekście multibranch pipeline. W przypadku zwykłego pipeline'u warto zamiast tego użyć warunku opartego na zmiennej `env.BRANCH_NAME` lub odpowiednio skonfigurować źródło branchy.
