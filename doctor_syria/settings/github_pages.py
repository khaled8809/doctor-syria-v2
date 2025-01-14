from .base import *

DEBUG = False

ALLOWED_HOSTS = ["khaled8809.github.io", "localhost", "127.0.0.1"]

# تكوين قاعدة البيانات SQLite للعرض فقط
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# إعدادات التخزين الثابت
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/doctor-syria-v2/static/"  # تحديث المسار ليتناسب مع GitHub Pages

# إعدادات الوسائط
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/doctor-syria-v2/media/"  # تحديث المسار ليتناسب مع GitHub Pages

# إعدادات الأمان
SECURE_SSL_REDIRECT = False  # تعطيل لأن GitHub Pages يتعامل مع SSL
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# إعدادات Whitenoise للملفات الثابتة
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# تعطيل CSRF للعرض فقط
CSRF_TRUSTED_ORIGINS = ["https://khaled8809.github.io"]

# تكوين البريد الإلكتروني للعرض
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
