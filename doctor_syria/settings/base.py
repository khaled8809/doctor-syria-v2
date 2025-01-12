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
    
    # Security apps
    'django_csp',
    'axes',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_ratelimit',
    'django_secure',
    'django_session_security',
    'django_user_sessions',
    'django_password_validators',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'django_filters',
    'drf_yasg',
    'channels',
    'allauth',
    'allauth.account',
    
    # Local apps
    'accounts',
    'appointments',
    'billing',
    'hospitals',
    'hr',
    'laboratory',
    'medical_records',
    'monitoring',
    'notifications',
    'pharmacy',
    'radiology',
    'security',
    'system_notifications',
    'analytics',
    'api',
    'core',
]

MIDDLEWARE = [
    # Security middleware
    'django.middleware.security.SecurityMiddleware',
    'django_csp.middleware.CSPMiddleware',
    'django_session_security.middleware.SessionSecurityMiddleware',
    'django_user_sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    
    # Standard middleware
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Custom security middleware
    'security.middleware.SecurityHeadersMiddleware',
    'security.middleware.ContentSecurityPolicyMiddleware',
    'security.middleware.XSSProtectionMiddleware',
    'security.middleware.SecureUploadMiddleware',
    'security.middleware.SQLInjectionProtectionMiddleware',
    'security.middleware.SecurityMonitoringMiddleware',
    
    # Rate limiting and brute force protection
    'axes.middleware.AxesMiddleware',
    'django_ratelimit.middleware.RatelimitMiddleware',
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
    'allauth.account.auth_backends.AuthenticationBackend',
]

from doctor_syria.security_config import (
    SECURITY_HEADERS,
    SESSION_SECURITY,
    PASSWORD_SECURITY,
    API_SECURITY,
    FILE_UPLOAD_SECURITY,
    DATABASE_SECURITY,
    CACHE_SECURITY,
    EMAIL_SECURITY,
    AUTH_SECURITY,
    CORS_SECURITY,
    RATE_LIMITING,
    SECURITY_MONITORING
)

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_USE_SESSIONS = True
X_FRAME_OPTIONS = SECURITY_HEADERS['X-Frame-Options']
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Content Security Policy
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'")
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_FONT_SRC = ("'self'", "https:", "data:")
CSP_CONNECT_SRC = ("'self'",)
CSP_OBJECT_SRC = ("'none'",)
CSP_BASE_URI = ("'self'",)
CSP_FRAME_ANCESTORS = ("'none'",)
CSP_FORM_ACTION = ("'self'",)
CSP_INCLUDE_NONCE_IN = ['script-src']
CSP_UPGRADE_INSECURE_REQUESTS = True

# Session Security
SESSION_SECURITY_WARN_AFTER = SESSION_SECURITY['WARN_AFTER'].total_seconds()
SESSION_SECURITY_EXPIRE_AFTER = SESSION_SECURITY['EXPIRE_AFTER'].total_seconds()
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Password Settings
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': PASSWORD_SECURITY['MIN_LENGTH'],
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'security.password_validation.PasswordStrengthValidator',
        'OPTIONS': {
            'min_length': 12,
            'special_chars': True,
            'numbers': True,
            'upper_case': True,
            'lower_case': True,
        }
    },
]

# Django Rest Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': RATE_LIMITING,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ) if not DEBUG else (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': API_SECURITY['JWT_EXPIRY'],
    'REFRESH_TOKEN_LIFETIME': API_SECURITY['REFRESH_TOKEN_EXPIRY'],
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

# Django Axes Settings
AXES_FAILURE_LIMIT = AUTH_SECURITY['MAX_LOGIN_ATTEMPTS']
AXES_LOCK_OUT_AT_FAILURE = True
AXES_COOLOFF_TIME = AUTH_SECURITY['LOCKOUT_DURATION'].total_seconds() / 3600  # Convert to hours
AXES_USE_USER_AGENT = True
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True
AXES_RESET_ON_SUCCESS = True
AXES_LOCKOUT_TEMPLATE = 'security/lockout.html'
AXES_LOCKOUT_URL = '/locked'
AXES_PROXY_COUNT = 0
AXES_META_PRECEDENCE_ORDER = [
    'HTTP_X_FORWARDED_FOR',
    'REMOTE_ADDR',
]

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = FILE_UPLOAD_SECURITY['MAX_UPLOAD_SIZE']
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
FILE_UPLOAD_HANDLERS = [
    'security.upload_handlers.VirusScanUploadHandler',
    'security.upload_handlers.ContentTypeValidationHandler',
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

# Input Validation
SANITIZE_USER_INPUT = True
HTML_SANITIZER_SETTINGS = {
    'tags': ['p', 'br', 'strong', 'em', 'u', 'a'],
    'attributes': {
        'a': ['href', 'title'],
    },
    'strip': True,
    'strip_comments': True,
}

# Database Settings
DATABASES = {
    'default': {
        **DATABASES['default'],
        'CONN_MAX_AGE': DATABASE_SECURITY['CONNECTION_TIMEOUT'],
        'OPTIONS': {
            'sslmode': 'require' if DATABASE_SECURITY['REQUIRE_SSL'] else 'prefer',
            'connect_timeout': DATABASE_SECURITY['CONNECTION_TIMEOUT'],
        },
    }
}

# Cache Settings
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.connection.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20,
            },
            'MAX_CONNECTIONS': 1000,
            'RETRY_ON_TIMEOUT': True,
            'PASSWORD': os.getenv('REDIS_PASSWORD'),
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            'IGNORE_EXCEPTIONS': True,
        },
        'KEY_PREFIX': CACHE_SECURITY['KEY_PREFIX'],
        'VERSION': CACHE_SECURITY['VERSION'],
        'TIMEOUT': CACHE_SECURITY['TIMEOUT'],
    }
}

# CORS Settings
CORS_ALLOW_CREDENTIALS = CORS_SECURITY['ALLOW_CREDENTIALS']
CORS_ALLOWED_ORIGINS = CORS_SECURITY['ALLOWED_ORIGINS']
CORS_ALLOWED_METHODS = CORS_SECURITY['ALLOWED_METHODS']
CORS_EXPOSE_HEADERS = CORS_SECURITY['EXPOSE_HEADERS']

# Email Settings
EMAIL_USE_TLS = EMAIL_SECURITY['USE_TLS']
EMAIL_VERIFICATION_TIMEOUT = EMAIL_SECURITY['VERIFICATION_EXPIRY'].total_seconds()

# Logging Configuration
if SECURITY_MONITORING['ENABLE_AUDIT_LOG']:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'file': {
                'level': SECURITY_MONITORING['LOG_LEVEL'],
                'class': 'logging.FileHandler',
                'filename': 'security.log',
                'formatter': 'verbose',
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
            },
        },
        'loggers': {
            'django.security': {
                'handlers': ['file', 'mail_admins'] if SECURITY_MONITORING['ALERT_ADMINS'] else ['file'],
                'level': SECURITY_MONITORING['LOG_LEVEL'],
                'propagate': True,
            },
        },
    }

# Security Monitoring
SECURITY_MONITORING_SETTINGS = {
    'ENABLE_AUDIT_LOG': True,
    'LOG_LEVEL': 'INFO',
    'ALERT_ADMINS': True,
    'ALERT_THRESHOLD': {
        'LOGIN_FAILURES': 5,
        'API_ERRORS': 50,
        'SECURITY_VIOLATIONS': 3,
    },
    'MONITOR_ENDPOINTS': True,
    'MONITOR_FILE_UPLOADS': True,
    'MONITOR_USER_ACTIONS': True,
    'MONITOR_DATABASE_QUERIES': True,
}

# Additional Security Settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SAMESITE = 'Strict'

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

# Email Security
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_TIMEOUT = 5
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = os.getenv('SERVER_EMAIL')

# Admin Security
ADMIN_URL = os.getenv('ADMIN_URL', 'admin/')
ADMINS = [
    ('Admin', os.getenv('ADMIN_EMAIL')),
]
MANAGERS = ADMINS

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/doctor_syria.log',
            'formatter': 'verbose',
        },
        'security': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/security.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['security', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        'doctor_syria': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
