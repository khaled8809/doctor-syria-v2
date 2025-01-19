"""
Development settings for the Doctor Syria project.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# السماح بجميع المضيفين في بيئة التطوير
ALLOWED_HOSTS = ["*"]

# قاعدة البيانات
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "doctor_syria_db",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# إعدادات البريد الإلكتروني
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# تكوين الوسائط والملفات الثابتة
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# تكوين الوسائط الثابتة
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# تكوين CORS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# الجلسات
SESSION_ENGINE = "django.contrib.sessions.backends.db"

# تكوين نموذج المستخدم المخصص
AUTH_USER_MODEL = "accounts.User"

# إعدادات اللغة
LANGUAGE_CODE = "ar"
TIME_ZONE = "Asia/Damascus"
USE_I18N = True
USE_TZ = True

# إعدادات الأمان في بيئة التطوير
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
