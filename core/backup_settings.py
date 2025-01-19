from datetime import datetime, timedelta
import os

# Backup Settings
BACKUP_SETTINGS = {
    'BACKUP_DIR': os.path.join('backups', 'db'),
    'MEDIA_BACKUP_DIR': os.path.join('backups', 'media'),
    
    # Backup Schedule
    'DAILY_BACKUP_TIME': '00:00',  # Midnight
    'WEEKLY_BACKUP_DAY': 'sunday',
    'MONTHLY_BACKUP_DAY': 1,  # First day of month
    
    # Retention Policy
    'DAILY_BACKUP_RETENTION': 7,    # Keep daily backups for 7 days
    'WEEKLY_BACKUP_RETENTION': 4,   # Keep weekly backups for 4 weeks
    'MONTHLY_BACKUP_RETENTION': 12, # Keep monthly backups for 12 months
    
    # Compression Settings
    'COMPRESSION': 'gzip',
    'COMPRESSION_LEVEL': 9,
    
    # Encryption Settings
    'ENCRYPT_BACKUPS': True,
    'ENCRYPTION_METHOD': 'AES-256',
    
    # Storage Settings
    'STORAGE_BACKEND': 'S3',  # Options: 'LOCAL', 'S3', 'AZURE'
    'S3_BUCKET': 'your-backup-bucket',
    'S3_PREFIX': 'doctor-syria-backups/',
    
    # Notification Settings
    'NOTIFY_ON_SUCCESS': True,
    'NOTIFY_ON_FAILURE': True,
    'NOTIFICATION_EMAIL': 'admin@your-domain.com',
    
    # Validation Settings
    'VALIDATE_BACKUP': True,
    'TEST_RESTORE': False,  # Set to True to test restore after backup
}

# Backup Naming Convention
def get_backup_filename():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f'backup_{timestamp}.sql.gz'

# Backup Rotation
def should_rotate_backup(filename):
    """Determine if a backup file should be rotated based on retention policy"""
    try:
        timestamp = datetime.strptime(filename.split('_')[1].split('.')[0], '%Y%m%d_%H%M%S')
        age = datetime.now() - timestamp
        
        if 'daily' in filename:
            return age > timedelta(days=BACKUP_SETTINGS['DAILY_BACKUP_RETENTION'])
        elif 'weekly' in filename:
            return age > timedelta(weeks=BACKUP_SETTINGS['WEEKLY_BACKUP_RETENTION'])
        elif 'monthly' in filename:
            return age > timedelta(days=30 * BACKUP_SETTINGS['MONTHLY_BACKUP_RETENTION'])
        return False
    except:
        return False
