# Prosty skrypt do backupu bazy danych w PowerShell

$DB_NAME = "app_database"
$BACKUP_DIR = "C:\var\backups\db"
$DATE = Get-Date -Format "yyyyMMdd_HHmmss"
$FILENAME = Join-Path $BACKUP_DIR "${DB_NAME}_${DATE}.sql.gz"
$TEMP_FILENAME = Join-Path $BACKUP_DIR "${DB_NAME}_${DATE}.sql"

# Sprawdz czy katalog istnieje
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
        Write-Host "Backup zakonczony sukcesem: $FILENAME"
    }
    finally {
        $gzipStream.Dispose()
        $outputStream.Dispose()
        $inputStream.Dispose()
        Remove-Item -Path $TEMP_FILENAME -Force
    }
}
else {
    Write-Error "Blad podczas wykonywania backupu!"
    if (Test-Path -Path $TEMP_FILENAME) {
        Remove-Item -Path $TEMP_FILENAME -Force
    }
    exit 1
}
