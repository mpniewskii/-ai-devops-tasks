#!/bin/bash

if systemctl is-active --quiet docker; then
echo "Usługa Docker działa poprawnie."
else
echo "Usługa Docker nie działa. Próba uruchomienia..."
sudo systemctl start docker

if systemctl is-active --quiet docker; then
    echo "Usługa Docker została pomyślnie uruchomiona."
else
    echo "Błąd: Nie udało się uruchomić usługi Docker."
    exit 1
fi


fi