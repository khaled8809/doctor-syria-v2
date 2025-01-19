"""
Django settings for doctor_syria project.
"""

import os
from datetime import timedelta
from pathlib import Path

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# Application definition
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'django_filters',
    'drf_yasg',
    'channels',
    'django_redis',
    'debug_toolbar',
    
    # Local apps
    'core.apps.CoreConfig',
    'accounts.apps.AccountsConfig',
    'doctors.apps.DoctorsConfig',
    'clinics.apps.ClinicsConfig',
    'appointments.apps.AppointmentsConfig',
    'medical_records.apps.MedicalRecordsConfig',
    'pharmacy.apps.PharmacyConfig',
    'laboratory.apps.LaboratoryConfig',
    'billing.apps.BillingConfig',
    'notifications.apps.NotificationsConfig',
    'ai_diagnosis.apps.AiDiagnosisConfig',
    'analytics.apps.AnalyticsConfig',
    'monitoring.apps.MonitoringConfig',
    'patient_records',
]

# Import additional settings
from .caching import *
from .rate_limiting import *

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "doctor_syria.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "doctor_syria.wsgi.application"
ASGI_APPLICATION = "doctor_syria.asgi.application"

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# إعدادات التخزين المؤقت
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL", "redis://localhost:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PARSER_CLASS": "redis.connection.HiredisParser",
            "SOCKET_TIMEOUT": 5,
            "SOCKET_CONNECT_TIMEOUT": 5,
            "CONNECTION_POOL_CLASS": "redis.BlockingConnectionPool",
            "CONNECTION_POOL_CLASS_KWARGS": {
                "max_connections": 50,
                "timeout": 20,
            },
            "MAX_CONNECTIONS": 1000,
            "RETRY_ON_TIMEOUT": True,
        },
    }
}

# استخدام Redis للجلسات
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# إعدادات ضغط الصور تلقائياً
IMAGEKIT_CACHEFILE_DIR = "CACHE/images"
IMAGEKIT_SPEC_CACHEFILE_NAMER = "imagekit.cachefiles.namers.hash"
IMAGEKIT_CACHE_BACKEND = "default"

# إعدادات تحسين الأداء
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB
FILE_UPLOAD_PERMISSIONS = 0o644
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# إعدادات Celery مع Redis
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Damascus"

# Internationalization
LANGUAGE_CODE = "ar"
TIME_ZONE = "Asia/Damascus"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# إعدادات الوسائط
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# إضافة مجلدات الباركود والبطاقات التعريفية
BARCODE_DIR = os.path.join(MEDIA_ROOT, "barcodes")
ID_CARDS_DIR = os.path.join(MEDIA_ROOT, "id_cards")

# إنشاء المجلدات إذا لم تكن موجودة
os.makedirs(BARCODE_DIR, exist_ok=True)
os.makedirs(ID_CARDS_DIR, exist_ok=True)

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model
AUTH_USER_MODEL = "accounts.User"

# Authentication settings
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "accounts:dashboard"
LOGOUT_REDIRECT_URL = "accounts:login"

# Authentication backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# Security Settings
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

# Session and Cookie Settings
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = True
CSRF_USE_SESSIONS = True
CSRF_COOKIE_NAME = "csrftoken"
CSRF_HEADER_NAME = "HTTP_X_CSRFTOKEN"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 12,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Rate Limiting
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = "default"
RATELIMIT_VIEW = "django.http.HttpResponseForbidden"

# REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

# JWT Settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# Channel Layers
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# Appointments settings
APPOINTMENT_SETTINGS = {
    "DEFAULT_DURATION": 30,  # Default appointment duration in minutes
    "REMINDER_BEFORE": 24,  # Send reminder 24 hours before appointment
    "MAX_APPOINTMENTS_PER_DAY": 20,  # Maximum appointments per day for a doctor
    "WORKING_HOURS": {
        "start": "09:00",
        "end": "17:00",
    },
    "BREAK_TIME": {
        "start": "13:00",
        "end": "14:00",
    },
}

# إعدادات نظام الإشعارات
NOTIFICATION_SETTINGS = {
    "EMAIL": {
        "ENABLED": True,
        "TEMPLATE_DIR": "notifications/email/",
        "FROM_EMAIL": "notifications@doctor-syria.com",
    },
    "SMS": {
        "ENABLED": True,
        "PROVIDER": "twilio",  # يمكن تغييره حسب مزود الخدمة
        "ACCOUNT_SID": os.getenv("SMS_ACCOUNT_SID", ""),
        "AUTH_TOKEN": os.getenv("SMS_AUTH_TOKEN", ""),
        "FROM_NUMBER": os.getenv("SMS_FROM_NUMBER", ""),
    },
    "WEBSOCKET": {
        "ENABLED": True,
        "RECONNECT_INTERVAL": 3000,  # بالميلي ثانية
        "MAX_RECONNECT_ATTEMPTS": 5,
    },
    "QUIET_HOURS": {
        "ENABLED": True,
        "DEFAULT_START": "22:00",
        "DEFAULT_END": "07:00",
    },
    "RETENTION": {
        "DAYS": 30,  # عدد الأيام للاحتفاظ بالإشعارات القديمة
        "MAX_PER_USER": 1000,  # الحد الأقصى للإشعارات لكل مستخدم
    },
}

# Notification settings
NOTIFICATION_SETTINGS = {
    "EMAIL_NOTIFICATIONS": True,
    "SMS_NOTIFICATIONS": True,
    "PUSH_NOTIFICATIONS": False,
    "NOTIFICATION_TYPES": [
        "appointment",
        "medical",
        "system",
    ],
}

# Medical Records settings
MEDICAL_RECORDS_SETTINGS = {
    "ENABLE_DIGITAL_SIGNATURES": True,
    "REQUIRE_DOCTOR_APPROVAL": True,
    "ENABLE_PATIENT_PORTAL": True,
    "ENABLE_LAB_INTEGRATION": True,
    "ENABLE_PHARMACY_INTEGRATION": True,
    "MEDICAL_RECORD_TYPES": [
        "general",
        "pediatric",
        "dental",
        "ophthalmology",
        "orthopedic",
    ],
    "LAB_TEST_CATEGORIES": [
        "blood",
        "urine",
        "imaging",
        "pathology",
        "genetic",
    ],
    "RADIOLOGY_TYPES": [
        "xray",
        "ct",
        "mri",
        "ultrasound",
        "other",
    ],
    "FILE_UPLOAD_SETTINGS": {
        "MAX_UPLOAD_SIZE": 10 * 1024 * 1024,  # 10MB
        "ALLOWED_EXTENSIONS": ["pdf", "jpg", "jpeg", "png", "dcm"],
        "STORAGE_BACKEND": "django.core.files.storage.FileSystemStorage",
    },
}

# إعدادات المراقبة
MONITORING_SETTINGS = {
    "ENABLED": True,
    "LOG_PERFORMANCE": True,
    "LOG_DATABASE_QUERIES": True,
    "METRIC_COLLECTION_INTERVAL": 60,  # ثواني
    "RETENTION_PERIOD": 30,  # أيام
    "ALERT_THRESHOLDS": {
        "cpu_usage": 80,  # نسبة مئوية
        "memory_usage": 80,  # نسبة مئوية
        "response_time": 2.0,  # ثواني
        "error_rate": 0.1,  # أخطاء في الثانية
    },
}

# إعدادات النسخ الاحتياطي
BACKUP_SETTINGS = {
    "BACKUP_DIR": os.path.join(BASE_DIR, "backups", "files"),
    "BACKUP_RETENTION_DAYS": 30,
    "COMPRESSION_ENABLED": True,
    "COMPRESSION_LEVEL": 6,
    "BACKUP_TYPES": {
        "full": {
            "schedule": "weekly",
            "day": "sunday",
            "time": "00:00",
        },
        "incremental": {
            "schedule": "daily",
            "time": "00:30",
        },
    },
    "NOTIFICATIONS": {
        "SUCCESS": True,
        "FAILURE": True,
        "EMAIL_ON_FAILURE": True,
    },
    "STORAGE_OPTIONS": {
        "LOCAL_PATH": os.path.join(BASE_DIR, "backups", "files"),
        "REMOTE_ENABLED": False,
        "REMOTE_PATH": os.getenv("BACKUP_REMOTE_PATH", ""),
        "REMOTE_ACCESS_KEY": os.getenv("BACKUP_REMOTE_ACCESS_KEY", ""),
        "REMOTE_SECRET_KEY": os.getenv("BACKUP_REMOTE_SECRET_KEY", ""),
    },
}

# إنشاء مجلد النسخ الاحتياطي
os.makedirs(BACKUP_SETTINGS["BACKUP_DIR"], exist_ok=True)

# إعدادات التسجيل
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "doctor_syria.log"),
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "verbose",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": True,
        },
        "doctor_syria": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

# Sentry Configuration
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
    environment=os.getenv("DJANGO_ENV", "development"),
)
