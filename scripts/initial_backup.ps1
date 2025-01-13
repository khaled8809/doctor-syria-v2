# Create backup directory
$backupDir = "backups"
New-Item -ItemType Directory -Force -Path $backupDir

# Backup timestamp
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

# Database backup
Write-Host "Creating database backup..."
docker-compose exec -T db pg_dump -U $env:DB_USER -d $env:DB_NAME > "$backupDir\db_backup_$timestamp.sql"

# Files backup
Write-Host "Creating files backup..."
Compress-Archive -Path "media/*" -DestinationPath "$backupDir\media_backup_$timestamp.zip" -Force

# Environment variables backup
Write-Host "Creating environment backup..."
Copy-Item ".env.production" "$backupDir\.env.production.backup_$timestamp"

Write-Host "Backup completed!"
Write-Host "Backup location: $backupDir"
