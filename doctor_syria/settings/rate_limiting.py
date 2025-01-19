# doctor_syria/settings/rate_limiting.py
"""Rate limiting configuration for the Doctor Syria project."""

# Rate limiting settings
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'
RATELIMIT_VIEW = True
RATELIMIT_FAIL_OPEN = False

# Define rate limits for different views
RATELIMIT_DEFAULT_LIMITS = {
    # Login attempts
    'login': '5/5m',  # 5 attempts per 5 minutes
    'password_reset': '3/1h',  # 3 attempts per hour
    
    # API endpoints
    'api': '1000/h',  # 1000 requests per hour for authenticated users
    'api-anon': '100/h',  # 100 requests per hour for anonymous users
    
    # Critical operations
    'appointment_create': '10/1h',  # 10 appointments per hour
    'medical_record_update': '20/1h',  # 20 medical record updates per hour
    
    # Search and listing
    'search': '60/1m',  # 60 searches per minute
    'list': '300/1h',  # 300 list requests per hour
}

# Custom rate limit groups
RATELIMIT_GROUPS = {
    'sensitive_operations': {
        'rate': '10/1h',
        'block': True,
        'paths': [
            '/api/medical-records/*',
            '/api/prescriptions/*',
            '/api/diagnoses/*',
        ],
    },
    'authentication': {
        'rate': '5/5m',
        'block': True,
        'paths': [
            '/api/auth/*',
            '/accounts/login/',
            '/accounts/register/',
        ],
    },
}

# Rate limit response settings
RATELIMIT_HEADER_PREFIX = 'X-RateLimit'
RATELIMIT_STATUS_CODE = 429  # Too Many Requests

# Rate limit exempt URLs
RATELIMIT_EXEMPT_URLS = [
    r'^/static/.*$',
    r'^/media/.*$',
    r'^/favicon\.ico$',
    r'^/robots\.txt$',
]
