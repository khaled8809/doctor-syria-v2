import os
import socket
import ssl
import sys
from datetime import datetime

import django
import requests
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "doctor_syria.settings.production")
django.setup()


class SecurityChecker:
    def __init__(self):
        self.issues = []
        self.warnings = []

    def check_debug_mode(self):
        """التحقق من وضع التصحيح"""
        if settings.DEBUG:
            self.issues.append("⚠️ وضع التصحيح DEBUG مفعل في الإنتاج")

    def check_secret_key(self):
        """التحقق من المفتاح السري"""
        if settings.SECRET_KEY in ["", "your-secret-key-here"]:
            self.issues.append("❌ المفتاح السري غير آمن أو فارغ")
        if len(settings.SECRET_KEY) < 50:
            self.warnings.append("⚠️ المفتاح السري قصير جداً")

    def check_ssl_certificate(self):
        """التحقق من شهادة SSL"""
        try:
            hostname = "doctor-syria.com"
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    expire_date = datetime.strptime(
                        cert["notAfter"], "%b %d %H:%M:%S %Y %Z"
                    )
                    if expire_date < datetime.now():
                        self.issues.append("❌ شهادة SSL منتهية الصلاحية")
                    else:
                        print("✅ شهادة SSL سارية المفعول")
        except Exception as e:
            self.issues.append(f"❌ خطأ في فحص شهادة SSL: {str(e)}")

    def check_security_headers(self):
        """التحقق من رؤوس الأمان"""
        try:
            response = requests.get("https://doctor-syria.com")
            headers = response.headers

            security_headers = {
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": ["DENY", "SAMEORIGIN"],
                "X-XSS-Protection": "1; mode=block",
                "Strict-Transport-Security": "max-age=31536000",
                "Content-Security-Policy": None,
            }

            for header, expected_value in security_headers.items():
                if header not in headers:
                    self.warnings.append(f"⚠️ الرأس {header} غير موجود")
                elif expected_value and headers[header] not in (
                    expected_value
                    if isinstance(expected_value, list)
                    else [expected_value]
                ):
                    self.warnings.append(f"⚠️ قيمة الرأس {header} غير صحيحة")
        except Exception as e:
            self.issues.append(f"❌ خطأ في فحص رؤوس الأمان: {str(e)}")

    def check_admin_url(self):
        """التحقق من URL لوحة الإدارة"""
        if "admin/" in settings.ADMIN_URL:
            self.warnings.append("⚠️ استخدام مسار افتراضي للوحة الإدارة")

    def check_database_configuration(self):
        """التحقق من إعدادات قاعدة البيانات"""
        db = settings.DATABASES["default"]
        if "sqlite" in db["ENGINE"]:
            self.warnings.append("⚠️ استخدام SQLite في الإنتاج")
        if not db.get("CONN_MAX_AGE"):
            self.warnings.append("⚠️ لم يتم تعيين CONN_MAX_AGE")

    def check_middleware(self):
        """التحقق من Middleware"""
        required_middleware = [
            "django.middleware.security.SecurityMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ]

        for middleware in required_middleware:
            if middleware not in settings.MIDDLEWARE:
                self.issues.append(f"❌ Middleware مفقود: {middleware}")

    def check_password_validators(self):
        """التحقق من التحقق من كلمات المرور"""
        if not settings.AUTH_PASSWORD_VALIDATORS:
            self.issues.append("❌ لم يتم تكوين التحقق من كلمات المرور")

    def run_all_checks(self):
        """تشغيل جميع الفحوصات الأمنية"""
        print("\n=== بدء فحص الأمان ===\n")

        checks = [
            self.check_debug_mode,
            self.check_secret_key,
            self.check_ssl_certificate,
            self.check_security_headers,
            self.check_admin_url,
            self.check_database_configuration,
            self.check_middleware,
            self.check_password_validators,
        ]

        for check in checks:
            try:
                check()
            except Exception as e:
                self.issues.append(f"❌ خطأ في {check.__name__}: {str(e)}")

        print("\n=== نتائج فحص الأمان ===\n")

        if self.issues:
            print("\n❌ المشاكل الأمنية:")
            for issue in self.issues:
                print(f"  - {issue}")

        if self.warnings:
            print("\n⚠️ التحذيرات الأمنية:")
            for warning in self.warnings:
                print(f"  - {warning}")

        if not self.issues and not self.warnings:
            print("\n✅ لم يتم العثور على مشاكل أمنية!")

        return len(self.issues) == 0


if __name__ == "__main__":
    checker = SecurityChecker()
    success = checker.run_all_checks()
    sys.exit(0 if success else 1)
