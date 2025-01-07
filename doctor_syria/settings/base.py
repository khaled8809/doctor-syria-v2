"""
Django settings for doctor_syria project.
"""

import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
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
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_ratelimit',
    
    # Local apps
    'accounts',
    'appointments',
    'system_notifications',
    'medical_records',
    'analytics',
    'notifications',
    'security',
    'billing',
    'hospitals',
    'monitoring',
    'core',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'doctor_syria.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'doctor_syria.wsgi.application'
ASGI_APPLICATION = 'doctor_syria.asgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'doctor_syria'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f"redis://{os.getenv('REDIS_HOST', 'localhost')}:"
                   f"{os.getenv('REDIS_PORT', '6379')}/1",
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Internationalization
LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Asia/Damascus'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# إعدادات الوسائط
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# إضافة مجلدات الباركود والبطاقات التعريفية
BARCODE_DIR = os.path.join(MEDIA_ROOT, 'barcodes')
ID_CARDS_DIR = os.path.join(MEDIA_ROOT, 'id_cards')

# إنشاء المجلدات إذا لم تكن موجودة
os.makedirs(BARCODE_DIR, exist_ok=True)
os.makedirs(ID_CARDS_DIR, exist_ok=True)

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'accounts.User'

# Authentication settings
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:dashboard'
LOGOUT_REDIRECT_URL = 'accounts:login'

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Security Settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Session and Cookie Settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_USE_SESSIONS = True
CSRF_COOKIE_NAME = 'csrftoken'
CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Rate Limiting
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'
RATELIMIT_VIEW = 'django.http.HttpResponseForbidden'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',') if not DEBUG else []

# Channel Layers
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(
                os.getenv('REDIS_HOST', 'localhost'),
                int(os.getenv('REDIS_PORT', 6379))
            )],
        },
    },
}

# Appointments settings
APPOINTMENT_SETTINGS = {
    'DEFAULT_DURATION': 30,  # Default appointment duration in minutes
    'REMINDER_BEFORE': 24,  # Send reminder 24 hours before appointment
    'MAX_APPOINTMENTS_PER_DAY': 20,  # Maximum appointments per day for a doctor
    'WORKING_HOURS': {
        'start': '09:00',
        'end': '17:00',
    },
    'BREAK_TIME': {
        'start': '13:00',
        'end': '14:00',
    },
}

# Notification settings
NOTIFICATION_SETTINGS = {
    'EMAIL_NOTIFICATIONS': True,
    'SMS_NOTIFICATIONS': True,
    'PUSH_NOTIFICATIONS': False,
    'NOTIFICATION_TYPES': [
        'appointment',
        'medical',
        'system',
    ],
}

# Medical Records settings
MEDICAL_RECORDS_SETTINGS = {
    'ENABLE_DIGITAL_SIGNATURES': True,
    'REQUIRE_DOCTOR_APPROVAL': True,
    'ENABLE_PATIENT_PORTAL': True,
    'ENABLE_LAB_INTEGRATION': True,
    'ENABLE_PHARMACY_INTEGRATION': True,
    'MEDICAL_RECORD_TYPES': [
        'general',
        'pediatric',
        'dental',
        'ophthalmology',
        'orthopedic',
    ],
    'LAB_TEST_CATEGORIES': [
        'blood',
        'urine',
        'imaging',
        'pathology',
        'genetic',
    ],
    'RADIOLOGY_TYPES': [
        'xray',
        'ct',
        'mri',
        'ultrasound',
        'other',
    ],
    'FILE_UPLOAD_SETTINGS': {
        'MAX_UPLOAD_SIZE': 10 * 1024 * 1024,  # 10MB
        'ALLOWED_EXTENSIONS': ['pdf', 'jpg', 'jpeg', 'png', 'dcm'],
        'STORAGE_BACKEND': 'django.core.files.storage.FileSystemStorage',
    }
}
