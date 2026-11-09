# Konwersja skryptu backupu bazy danych z Bash na PowerShell

## Zapytanie (Prompt)

> Przekonwertuj ten skrypt bash na równoważny skrypt PowerShell dla Windows.

## 1. Oryginalna wersja Bash

Oryginalny skrypt znajduje się w pliku [backup-db.sh](./backup-db.sh).

```bash
#!/bin/bash
# Prosty skrypt do backupu bazy danych

DB_NAME="app_database"
BACKUP_DIR="/var/backups/db"
DATE=$(date +%Y%m%d_%H%M%S)
FILENAME="${BACKUP_DIR}/${DB_NAME}_${DATE}.sql.gz"

# Sprawdź czy katalog istnieje
if [ ! -d "$BACKUP_DIR" ]; then
  mkdir -p "$BACKUP_DIR"
  echo "Utworzono katalog $BACKUP_DIR"
fi

# Wykonaj backup
echo "Rozpoczynam backup bazy $DB_NAME..."
mysqldump -u root -p "$DB_NAME" | gzip > "$FILENAME"

if [ $? -eq 0 ]; then
  echo "Backup zakończony sukcesem: $FILENAME"
else
  echo "Błąd podczas wykonywania backupu!"
  exit 1
fi
```

## 2. Wersja PowerShell

Przekonwertowany skrypt znajduje się w pliku [backup-db.ps1](./backup-db.ps1).

```powershell
# Prosty skrypt do backupu bazy danych w PowerShell

$DB_NAME = "app_database"
$BACKUP_DIR = "C:\var\backups\db"
$DATE = Get-Date -Format "yyyyMMdd_HHmmss"
$FILENAME = Join-Path $BACKUP_DIR "${DB_NAME}_${DATE}.sql.gz"
$TEMP_FILENAME = Join-Path $BACKUP_DIR "${DB_NAME}_${DATE}.sql"

# Sprawdź czy katalog istnieje
if (-not (Test-Path -Path $BACKUP_DIR -PathType Container)) {
    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null
    Write-Host "Utworzono katalog $BACKUP_DIR"
}

# Wykonaj backup
Write-Host "Rozpoczynam backup bazy $DB_NAME..."
& mysqldump -u root -p $DB_NAME | Out-File -FilePath $TEMP_FILENAME -Encoding utf8
$dumpExitCode = $LASTEXITCODE

if ($dumpExitCode -eq 0) {
    $inputStream = [System.IO.File]::OpenRead($TEMP_FILENAME)
    $outputStream = [System.IO.File]::Create($FILENAME)
    $gzipStream = [System.IO.Compression.GZipStream]::new(
        $outputStream,
        [System.IO.Compression.CompressionMode]::Compress
    )

    try {
        $inputStream.CopyTo($gzipStream)
        Write-Host "Backup zakończony sukcesem: $FILENAME"
    }
    finally {
        $gzipStream.Dispose()
        $outputStream.Dispose()
        $inputStream.Dispose()
        Remove-Item -Path $TEMP_FILENAME -Force
    }
}
else {
    Write-Error "Błąd podczas wykonywania backupu!"
    if (Test-Path -Path $TEMP_FILENAME) {
        Remove-Item -Path $TEMP_FILENAME -Force
    }
    exit 1
}
```

## 3. Główne różnice między Bash i PowerShell

### Zmienne

* W Bash zmienne są zapisywane bez prefiksu, np. `DB_NAME`.
* W PowerShell zmienne zawsze zaczynają się od znaku `$`, np. `$DB_NAME`.

### Ścieżki i tworzenie katalogów

* Bash używa ścieżek z ukośnikami, np. `/var/backups/db`.
* PowerShell dla Windows używa ścieżki `C:\var\backups\db`.
* Polecenie `mkdir -p` zostało zastąpione przez `New-Item -ItemType Directory -Force`.
* Do sprawdzenia istnienia katalogu użyto `Test-Path`, a nie testu `[ -d ... ]`.

### Data i nazwa pliku

* Bash formatuje datę poleceniem `date`.
* PowerShell używa `Get-Date -Format`.
* Funkcja `Join-Path` bezpiecznie łączy katalog i nazwę pliku, zamiast ręcznego sklejania ścieżki.

### Uruchamianie poleceń i potoki

* W Bash polecenia są łączone operatorem potoku `|`, a wynik jest przekazywany do programu `gzip`.
* W PowerShell polecenie zewnętrzne uruchamiane jest operatorem `&`, a wynik `mysqldump` trafia do pliku tymczasowego przez `Out-File`.
* Do utworzenia pliku `.gz` wykorzystano klasę .NET `GZipStream`, dostępną bez instalowania osobnego programu `gzip`.

### Obsługa kodu zakończenia i błędów

* Bash korzysta ze specjalnej zmiennej `$?`, która zawiera status ostatniego polecenia.
* PowerShell wykorzystuje `$LASTEXITCODE` do odczytania kodu zakończenia programu zewnętrznego.
* Blok `try/finally` gwarantuje zamknięcie strumieni i usunięcie pliku tymczasowego po kompresji.

## 4. Zachowane działanie

Oba skrypty:

1. Sprawdzają, czy katalog backupu istnieje, i tworzą go w razie potrzeby.
2. Uruchamiają `mysqldump` dla bazy `app_database`.
3. Tworzą skompresowany plik backupu z datą i godziną w nazwie.
4. Wyświetlają komunikat o sukcesie lub błędzie.
5. Zwracają kod `1`, jeśli wykonanie backupu nie powiedzie się.
