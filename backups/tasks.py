"""
مهام Celery للنسخ الاحتياطي
"""

from celery import shared_task
from django.conf import settings

from .backup_manager import BackupManager


@shared_task
def create_automated_backup():
    """مهمة إنشاء نسخة احتياطية تلقائية"""
    manager = BackupManager()
    return manager.create_backup(backup_type="full")


@shared_task
def create_incremental_backup():
    """مهمة إنشاء نسخة احتياطية تزايدية"""
    manager = BackupManager()
    return manager.create_backup(backup_type="incremental")


@shared_task
def cleanup_old_backups():
    """مهمة تنظيف النسخ الاحتياطية القديمة"""
    manager = BackupManager()
    retention_days = getattr(settings, "BACKUP_RETENTION_DAYS", 30)
    return manager.cleanup_old_backups(days_to_keep=retention_days)


# جدولة المهام
from celery.schedules import crontab

from doctor_syria.celery import app

# نسخة احتياطية كاملة كل أسبوع
app.conf.beat_schedule.update(
    {
        "weekly-full-backup": {
            "task": "backups.tasks.create_automated_backup",
            "schedule": crontab(hour=0, minute=0, day_of_week=0),
        },
    }
)

# نسخة احتياطية تزايدية يومياً
app.conf.beat_schedule.update(
    {
        "daily-incremental-backup": {
            "task": "backups.tasks.create_incremental_backup",
            "schedule": crontab(hour=0, minute=30),
        },
    }
)

# تنظيف النسخ الاحتياطية القديمة كل شهر
app.conf.beat_schedule.update(
    {
        "monthly-backup-cleanup": {
            "task": "backups.tasks.cleanup_old_backups",
            "schedule": crontab(hour=1, minute=0, day_of_month=1),
        },
    }
)
