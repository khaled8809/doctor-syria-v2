import os
import shutil
import sys
import time
from datetime import datetime

import boto3
import django
from django.conf import settings
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "doctor_syria.settings.production")
django.setup()


class BackupManager:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = os.path.join(settings.BASE_DIR, "backups")
        self.ensure_backup_dir()

        # تهيئة AWS S3
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )

    def ensure_backup_dir(self):
        """التأكد من وجود مجلد النسخ الاحتياطي"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def backup_database(self):
        """نسخ احتياطي لقاعدة البيانات"""
        print("جارٍ نسخ قاعدة البيانات...")
        backup_file = os.path.join(self.backup_dir, f"db_backup_{self.timestamp}.json")
        try:
            with open(backup_file, "w", encoding="utf-8") as f:
                call_command("dumpdata", "--indent", "2", stdout=f)
            print(f"✅ تم نسخ قاعدة البيانات إلى: {backup_file}")
            return backup_file
        except Exception as e:
            print(f"❌ فشل نسخ قاعدة البيانات: {str(e)}")
            return None

    def backup_media(self):
        """نسخ احتياطي لملفات الوسائط"""
        print("جارٍ نسخ ملفات الوسائط...")
        media_backup = os.path.join(
            self.backup_dir, f"media_backup_{self.timestamp}.zip"
        )
        try:
            shutil.make_archive(
                media_backup[:-4], "zip", settings.MEDIA_ROOT  # remove .zip
            )
            print(f"✅ تم نسخ ملفات الوسائط إلى: {media_backup}")
            return media_backup
        except Exception as e:
            print(f"❌ فشل نسخ ملفات الوسائط: {str(e)}")
            return None

    def upload_to_s3(self, file_path):
        """رفع النسخة الاحتياطية إلى S3"""
        if not file_path or not os.path.exists(file_path):
            return False

        print(f"جارٍ الرفع إلى S3: {file_path}")
        try:
            file_name = os.path.basename(file_path)
            self.s3.upload_file(
                file_path, settings.AWS_STORAGE_BUCKET_NAME, f"backups/{file_name}"
            )
            print(f"✅ تم الرفع إلى S3: {file_name}")
            return True
        except Exception as e:
            print(f"❌ فشل الرفع إلى S3: {str(e)}")
            return False

    def cleanup_old_backups(self, days=7):
        """حذف النسخ الاحتياطية القديمة"""
        print("جارٍ تنظيف النسخ الاحتياطية القديمة...")
        current_time = time.time()

        for filename in os.listdir(self.backup_dir):
            file_path = os.path.join(self.backup_dir, filename)
            if os.path.isfile(file_path):
                if os.stat(file_path).st_mtime < (current_time - (days * 86400)):
                    try:
                        os.remove(file_path)
                        print(f"✅ تم حذف الملف القديم: {filename}")
                    except Exception as e:
                        print(f"❌ فشل حذف الملف: {filename} - {str(e)}")

    def run_backup(self):
        """تنفيذ عملية النسخ الاحتياطي الكاملة"""
        print("\n=== بدء عملية النسخ الاحتياطي ===\n")

        # نسخ قاعدة البيانات
        db_backup = self.backup_database()
        if db_backup:
            self.upload_to_s3(db_backup)

        # نسخ ملفات الوسائط
        media_backup = self.backup_media()
        if media_backup:
            self.upload_to_s3(media_backup)

        # تنظيف النسخ القديمة
        self.cleanup_old_backups()

        print("\n=== اكتملت عملية النسخ الاحتياطي ===\n")


if __name__ == "__main__":
    backup_manager = BackupManager()
    backup_manager.run_backup()
