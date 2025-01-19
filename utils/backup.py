import logging
import os
import subprocess
from datetime import datetime

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import DatabaseError

logger = logging.getLogger(__name__)


class BackupError(Exception):
    """استثناء مخصص لأخطاء النسخ الاحتياطي"""

    pass


class BackupService:
    def __init__(self):
        try:
            self.s3 = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
            )
            self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        except (AttributeError, ClientError) as e:
            logger.error(f"خطأ في تهيئة خدمة S3: {str(e)}")
            raise BackupError("فشل في الاتصال بخدمة التخزين السحابي")

    def create_database_backup(self):
        """إنشاء نسخة احتياطية من قاعدة البيانات"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_db_{timestamp}.json"
        filepath = os.path.join(settings.BACKUP_DIR, filename)

        try:
            # إنشاء مجلد النسخ الاحتياطي إذا لم يكن موجوداً
            os.makedirs(settings.BACKUP_DIR, exist_ok=True)

            # إنشاء نسخة احتياطية من قاعدة البيانات
            with open(filepath, "w") as f:
                call_command(
                    "dumpdata",
                    exclude=["contenttypes", "auth.Permission"],
                    output=f.name,
                )

            # رفع النسخة الاحتياطية إلى S3
            self.upload_to_s3(filepath, f"database_backups/{filename}")

            logger.info(f"تم إنشاء نسخة احتياطية بنجاح: {filename}")
            return True

        except OSError as e:
            logger.error(f"خطأ في إنشاء مجلد النسخ الاحتياطي: {str(e)}")
            raise BackupError("فشل في إنشاء مجلد النسخ الاحتياطي")
        except CommandError as e:
            logger.error(f"خطأ في إنشاء نسخة احتياطية من قاعدة البيانات: {str(e)}")
            raise BackupError("فشل في إنشاء نسخة احتياطية من قاعدة البيانات")
        except DatabaseError as e:
            logger.error(f"خطأ في قاعدة البيانات: {str(e)}")
            raise BackupError("فشل في الوصول إلى قاعدة البيانات")

    def create_media_backup(self):
        """إنشاء نسخة احتياطية من ملفات الوسائط"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_media_{timestamp}.tar.gz"
        filepath = os.path.join(settings.BACKUP_DIR, filename)

        try:
            # ضغط مجلد الوسائط
            subprocess.run(["tar", "-czf", filepath, settings.MEDIA_ROOT], check=True)

            # رفع النسخة الاحتياطية إلى S3
            self.upload_to_s3(filepath, f"media_backups/{filename}")

            logger.info(f"تم إنشاء نسخة احتياطية للوسائط بنجاح: {filename}")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"خطأ في ضغط ملفات الوسائط: {str(e)}")
            raise BackupError("فشل في ضغط ملفات الوسائط")
        except OSError as e:
            logger.error(f"خطأ في الوصول إلى ملفات الوسائط: {str(e)}")
            raise BackupError("فشل في الوصول إلى ملفات الوسائط")

    def upload_to_s3(self, file_path, s3_path):
        """رفع الملف إلى S3"""
        try:
            self.s3.upload_file(file_path, self.bucket_name, s3_path)
            # حذف الملف المحلي بعد الرفع
            os.remove(file_path)
            return True
        except ClientError as e:
            logger.error(f"خطأ في رفع الملف إلى S3: {str(e)}")
            raise BackupError("فشل في رفع الملف إلى خدمة التخزين السحابي")
        except OSError as e:
            logger.error(f"خطأ في حذف الملف المحلي: {str(e)}")
            raise BackupError("فشل في حذف الملف المحلي")

    def restore_from_backup(self, backup_file):
        """استعادة من نسخة احتياطية"""
        try:
            # تنزيل النسخة الاحتياطية من S3
            local_path = os.path.join(
                settings.BACKUP_DIR, os.path.basename(backup_file)
            )
            self.s3.download_file(self.bucket_name, backup_file, local_path)

            # استعادة قاعدة البيانات
            if backup_file.startswith("database_backups/"):
                call_command("loaddata", local_path)

            # استعادة ملفات الوسائط
            elif backup_file.startswith("media_backups/"):
                subprocess.run(
                    ["tar", "-xzf", local_path, "-C", settings.MEDIA_ROOT], check=True
                )

            # حذف الملف المحلي بعد الاستعادة
            os.remove(local_path)
            logger.info(f"تم استعادة النسخة الاحتياطية بنجاح: {backup_file}")
            return True

        except ClientError as e:
            logger.error(f"خطأ في تنزيل النسخة الاحتياطية من S3: {str(e)}")
            raise BackupError("فشل في تنزيل النسخة الاحتياطية")
        except CommandError as e:
            logger.error(f"خطأ في استعادة قاعدة البيانات: {str(e)}")
            raise BackupError("فشل في استعادة قاعدة البيانات")
        except subprocess.CalledProcessError as e:
            logger.error(f"خطأ في فك ضغط ملفات الوسائط: {str(e)}")
            raise BackupError("فشل في فك ضغط ملفات الوسائط")
        except OSError as e:
            logger.error(f"خطأ في الوصول إلى الملفات: {str(e)}")
            raise BackupError("فشل في الوصول إلى الملفات")
