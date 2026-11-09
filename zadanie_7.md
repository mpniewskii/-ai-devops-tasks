# Wyjaśnienie działania skryptu `check_docker.sh`

Oto szczegółowe omówienie działania skryptu linia po linii dla osoby początkującej:

```bash
#!/bin/bash
```
* **Linia 1:** Tzw. *Shebang* (`#!`). Wskazuje systemowi operacyjnemu, jakiego interpretera ma użyć do wykonania tego pliku – w tym przypadku jest to `/bin/bash`.

```bash
if systemctl is-active --quiet docker; then
```
* **Linia 3:** Instrukcja warunkowa `if`. Sprawdza stan usługi Docker za pomocą narzędzia `systemctl`. Flaga `--quiet` ukrywa domyślne wyjście z terminala, a sam warunek przechodzi pomyślnie (zwraca kod `0`), jeśli usługa jest aktywna.

```bash
    echo "Usługa Docker działa poprawnie."
```
* **Linia 4:** Wyświetla komunikat w konsoli, gdy usługa Docker już działa.

```bash
else
```
* **Linia 5:** Część warunku wykonująca się wtedy, gdy Docker **nie jest** aktywny.

```bash
    echo "Usługa Docker nie działa. Próba uruchomienia..."
```
* **Linia 6:** Informuje użytkownika o podjęciu próby uruchomienia usługi.

```bash
    sudo systemctl start docker
```
* **Linia 7:** Polecenie uruchamiające usługę Docker. Wymaga uprawnień administratora (`sudo`).

```bash
    if systemctl is-active --quiet docker; then
```
* **Linia 9:** Drugie sprawdzenie statusu usługi w celu weryfikacji, czy próba uruchomienia zakończyła się sukcesem.

```bash
        echo "Usługa Docker została pomyślnie uruchomiona."
```
* **Linia 10:** Informuje o pomyślnym podniesieniu usługi Docker.

```bash
    else
```
* **Linia 11:** Część wykonywana w przypadku niepowodzenia przy próbie uruchomienia.

```bash
        echo "Błąd: Nie udało się uruchomić usługi Docker."
```
* **Linia 12:** Komunikat o błędzie.

```bash
        exit 1
```
* **Linia 13:** Zakończenie działania skryptu z kodem wyjścia `1`, co oznacza wystąpienie błędu.

```bash
    fi
fi
```
* **Linie 14 i 15:** Zakończenie bloku instrukcji warunkowych `if` (słowo `fi` to odwrócone `if`).