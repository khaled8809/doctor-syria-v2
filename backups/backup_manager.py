"""
مدير النسخ الاحتياطي
"""

import gzip
import logging
import os
import shutil
import subprocess
from datetime import datetime

from django.conf import settings
from django.core.management import call_command
from django.utils import timezone

from .models import BackupJob, RestorePoint

logger = logging.getLogger(__name__)


class BackupManager:
    """مدير النسخ الاحتياطي"""

    def __init__(self):
        self.backup_dir = os.path.join(settings.BASE_DIR, "backups", "files")
        os.makedirs(self.backup_dir, exist_ok=True)

    def create_backup(self, backup_type="full"):
        """إنشاء نسخة احتياطية جديدة"""

        # إنشاء مهمة نسخ احتياطي جديدة
        backup_job = BackupJob.objects.create(backup_type=backup_type, status="running")

        try:
            # إنشاء اسم الملف
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"backup_{backup_type}_{timestamp}.json.gz"
            filepath = os.path.join(self.backup_dir, filename)

            # تنفيذ النسخ الاحتياطي
            with gzip.open(filepath, "wb") as f:
                call_command(
                    "dumpdata",
                    exclude=["contenttypes", "auth.permission"],
                    natural_foreign=True,
                    natural_primary=True,
                    stdout=f,
                )

            # تحديث معلومات المهمة
            backup_job.status = "completed"
            backup_job.completed_at = timezone.now()
            backup_job.file_path = filepath
            backup_job.file_size = os.path.getsize(filepath)
            backup_job.save()

            # إنشاء نقطة استعادة
            RestorePoint.objects.create(
                backup=backup_job,
                description=f"نسخة احتياطية {backup_type}",
                is_automated=True,
                metadata={
                    "database_version": self.get_db_version(),
                    "django_version": self.get_django_version(),
                    "backup_size": backup_job.get_file_size_display(),
                },
            )

            logger.info(f"تم إنشاء نسخة احتياطية بنجاح: {filename}")
            return backup_job

        except Exception as e:
            backup_job.status = "failed"
            backup_job.error_message = str(e)
            backup_job.completed_at = timezone.now()
            backup_job.save()
            logger.error(f"فشل في إنشاء النسخة الاحتياطية: {str(e)}")
            raise

    def restore_backup(self, backup_job):
        """استعادة من نسخة احتياطية"""

        if not os.path.exists(backup_job.file_path):
            raise FileNotFoundError("ملف النسخة الاحتياطية غير موجود")

        try:
            # إنشاء نسخة احتياطية قبل الاستعادة
            self.create_backup(backup_type="pre_restore")

            # استعادة البيانات
            with gzip.open(backup_job.file_path, "rb") as f:
                call_command("loaddata", "-", stdin=f)

            logger.info(f"تم استعادة النسخة الاحتياطية بنجاح: {backup_job.file_path}")
            return True

        except Exception as e:
            logger.error(f"فشل في استعادة النسخة الاحتياطية: {str(e)}")
            raise

    def cleanup_old_backups(self, days_to_keep=30):
        """تنظيف النسخ الاحتياطية القديمة"""

        cutoff_date = timezone.now() - timezone.timedelta(days=days_to_keep)
        old_backups = BackupJob.objects.filter(
            started_at__lt=cutoff_date, status="completed"
        )

        for backup in old_backups:
            try:
                if backup.file_path and os.path.exists(backup.file_path):
                    os.remove(backup.file_path)
                backup.delete()
                logger.info(f"تم حذف النسخة الاحتياطية القديمة: {backup.file_path}")
            except Exception as e:
                logger.error(f"فشل في حذف النسخة الاحتياطية: {str(e)}")

    @staticmethod
    def get_db_version():
        """الحصول على إصدار قاعدة البيانات"""
        try:
            with subprocess.Popen(
                ["psql", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            ) as proc:
                version = proc.stdout.read().decode()
                return version.strip()
        except:
            return "Unknown"

    @staticmethod
    def get_django_version():
        """الحصول على إصدار Django"""
        import django

        return django.get_version()
