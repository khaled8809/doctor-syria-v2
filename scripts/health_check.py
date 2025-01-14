import os
import sys

import django
import psutil
import requests
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.db import connections
from redis import Redis

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "doctor_syria.settings.production")
django.setup()


class SystemHealthCheck:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def check_database(self):
        """التحقق من اتصال قاعدة البيانات"""
        try:
            for name in connections.databases:
                cursor = connections[name].cursor()
                cursor.execute("SELECT 1")
                row = cursor.fetchone()
                if row is None:
                    self.errors.append(f"فشل الاتصال بقاعدة البيانات {name}")
                else:
                    print(f"✅ الاتصال بقاعدة البيانات {name} يعمل بشكل صحيح")
        except Exception as e:
            self.errors.append(f"خطأ في قاعدة البيانات: {str(e)}")

    def check_redis(self):
        """التحقق من اتصال Redis"""
        try:
            redis_client = Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD,
            )
            if redis_client.ping():
                print("✅ الاتصال بـ Redis يعمل بشكل صحيح")
            else:
                self.errors.append("فشل الاتصال بـ Redis")
        except Exception as e:
            self.errors.append(f"خطأ في Redis: {str(e)}")

    def check_disk_space(self):
        """التحقق من مساحة القرص"""
        disk = psutil.disk_usage("/")
        if disk.percent > 85:
            self.warnings.append(f"تحذير: مساحة القرص مرتفعة ({disk.percent}%)")
        else:
            print(f"✅ مساحة القرص متوفرة ({disk.percent}%)")

    def check_memory(self):
        """التحقق من استخدام الذاكرة"""
        memory = psutil.virtual_memory()
        if memory.percent > 90:
            self.warnings.append(f"تحذير: استخدام الذاكرة مرتفع ({memory.percent}%)")
        else:
            print(f"✅ استخدام الذاكرة طبيعي ({memory.percent}%)")

    def check_static_files(self):
        """التحقق من الملفات الثابتة"""
        static_root = settings.STATIC_ROOT
        if not os.path.exists(static_root):
            self.errors.append("مجلد STATIC_ROOT غير موجود")
        else:
            print("✅ مجلد الملفات الثابتة موجود")

    def check_media_files(self):
        """التحقق من مجلد الوسائط"""
        media_root = settings.MEDIA_ROOT
        if not os.path.exists(media_root):
            self.errors.append("مجلد MEDIA_ROOT غير موجود")
        else:
            print("✅ مجلد الوسائط موجود")

    def check_ssl_certificate(self):
        """التحقق من شهادة SSL"""
        try:
            response = requests.get("https://doctor-syria.com", verify=True)
            print("✅ شهادة SSL تعمل بشكل صحيح")
        except requests.exceptions.SSLError:
            self.errors.append("خطأ في شهادة SSL")
        except requests.exceptions.RequestException:
            self.warnings.append("لم نتمكن من التحقق من شهادة SSL")

    def check_required_directories(self):
        """التحقق من وجود المجلدات المطلوبة"""
        required_dirs = [
            settings.STATIC_ROOT,
            settings.MEDIA_ROOT,
            os.path.join(settings.BASE_DIR, "logs"),
            os.path.join(settings.BASE_DIR, "backups"),
        ]

        for directory in required_dirs:
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                    print(f"✅ تم إنشاء المجلد: {directory}")
                except Exception as e:
                    self.errors.append(f"فشل إنشاء المجلد {directory}: {str(e)}")
            else:
                print(f"✅ المجلد موجود: {directory}")

    def run_all_checks(self):
        """تشغيل جميع الفحوصات"""
        print("\n=== بدء فحص النظام ===\n")

        checks = [
            self.check_database,
            self.check_redis,
            self.check_disk_space,
            self.check_memory,
            self.check_static_files,
            self.check_media_files,
            self.check_ssl_certificate,
            self.check_required_directories,
        ]

        for check in checks:
            try:
                check()
            except Exception as e:
                self.errors.append(f"خطأ في {check.__name__}: {str(e)}")

        print("\n=== نتائج الفحص ===\n")

        if self.errors:
            print("\n❌ الأخطاء:")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print("\n⚠️ التحذيرات:")
            for warning in self.warnings:
                print(f"  - {warning}")

        if not self.errors and not self.warnings:
            print("\n✅ جميع الفحوصات ناجحة!")

        return len(self.errors) == 0


if __name__ == "__main__":
    checker = SystemHealthCheck()
    success = checker.run_all_checks()
    sys.exit(0 if success else 1)
