# doctor_syria/settings/caching.py
"""Caching configuration for the Doctor Syria project."""

# Cacheops configuration
CACHEOPS_REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 1,
    'socket_timeout': 3,
}

CACHEOPS = {
    # Cache all models in the auth app for 12 hours
    'auth.*': {'ops': 'all', 'timeout': 12*60*60},
    
    # Cache all models in accounts app
    'accounts.*': {'ops': 'all', 'timeout': 12*60*60},
    
    # Cache all models in clinics app
    'clinics.*': {'ops': 'all', 'timeout': 12*60*60},
    
    # Cache all models in doctors app
    'doctors.*': {'ops': 'all', 'timeout': 12*60*60},
    
    # Cache specific models with different timeouts
    'appointments.Appointment': {'ops': 'all', 'timeout': 6*60*60},
    'medical_records.Record': {'ops': 'all', 'timeout': 24*60*60},
    
    # Cache all other models for 1 hour
    '*.*': {'ops': 'all', 'timeout': 60*60},
}

# Django's cache settings
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            'IGNORE_EXCEPTIONS': True,
        }
    }
}

# Cache session backend
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Cache middleware settings
CACHE_MIDDLEWARE_SECONDS = 60 * 15  # 15 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'doctor_syria'

# Template fragment caching
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)
