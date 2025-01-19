#!/bin/bash

# Load environment variables
source /path/to/your/env/file

# Set backup directory
BACKUP_DIR="${BACKUP_DIR:-/var/backups/doctor_syria}"
BACKUP_RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-30}"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Get current timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Backup database
pg_dump -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -F c -f "$BACKUP_DIR/db_backup_$TIMESTAMP.dump"

# Backup media files
tar -czf "$BACKUP_DIR/media_backup_$TIMESTAMP.tar.gz" -C /var/www/doctor_syria media/

# Backup configuration files
tar -czf "$BACKUP_DIR/config_backup_$TIMESTAMP.tar.gz" /etc/nginx/sites-available/doctor_syria /etc/supervisor/conf.d/doctor_syria.conf

# Remove old backups
find "$BACKUP_DIR" -type f -mtime +$BACKUP_RETENTION_DAYS -delete

# Optional: Upload to S3 or another remote storage
if [ -n "$AWS_ACCESS_KEY_ID" ] && [ -n "$AWS_SECRET_ACCESS_KEY" ]; then
    aws s3 sync "$BACKUP_DIR" "s3://$AWS_STORAGE_BUCKET_NAME/backups/"
fi

# Log backup completion
echo "Backup completed at $(date)" >> "$BACKUP_DIR/backup.log"
