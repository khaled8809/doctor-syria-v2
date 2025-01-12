"""
Security configuration for Doctor Syria Platform
"""

from datetime import timedelta

# Security Headers Configuration
SECURITY_HEADERS = {
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'X-Content-Type-Options': 'nosniff',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Content-Security-Policy': (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' data: https:; "
        "connect-src 'self'; "
        "frame-ancestors 'none'; "
        "form-action 'self'"
    ),
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
    'Cross-Origin-Opener-Policy': 'same-origin',
    'Cross-Origin-Embedder-Policy': 'require-corp',
    'Cross-Origin-Resource-Policy': 'same-origin',
}

# Session Security Configuration
SESSION_SECURITY = {
    'EXPIRE_AFTER': timedelta(minutes=30),
    'WARN_AFTER': timedelta(minutes=25),
    'PASSIVE_URL_NAMES': ['password_reset', 'logout', 'login'],
    'LOGOUT_URL': '/logout/',
    'LOGIN_URL': '/login/',
}

# Password Security Configuration
PASSWORD_SECURITY = {
    'MIN_LENGTH': 12,
    'SPECIAL_CHARS_REQUIRED': True,
    'NUMBERS_REQUIRED': True,
    'UPPERCASE_REQUIRED': True,
    'LOWERCASE_REQUIRED': True,
    'PREVENT_COMMON_PASSWORDS': True,
    'PASSWORD_HISTORY': 5,
    'MAX_PASSWORD_AGE': 90,  # days
}

# API Security Configuration
API_SECURITY = {
    'MAX_REQUESTS_PER_MINUTE': 60,
    'MAX_REQUESTS_PER_HOUR': 1000,
    'REQUIRE_HTTPS': True,
    'API_KEY_HEADER': 'X-API-Key',
    'JWT_EXPIRY': timedelta(minutes=15),
    'REFRESH_TOKEN_EXPIRY': timedelta(days=7),
}

# File Upload Security Configuration
FILE_UPLOAD_SECURITY = {
    'MAX_UPLOAD_SIZE': 5242880,  # 5MB
    'ALLOWED_FILE_TYPES': [
        'image/jpeg',
        'image/png',
        'image/gif',
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    ],
    'SCAN_UPLOADS': True,
    'SANITIZE_FILENAMES': True,
}

# Database Security Configuration
DATABASE_SECURITY = {
    'CONNECTION_TIMEOUT': 5,
    'REQUIRE_SSL': True,
    'MAX_POOL_SIZE': 20,
    'STATEMENT_TIMEOUT': 30000,  # milliseconds
}

# Cache Security Configuration
CACHE_SECURITY = {
    'KEY_PREFIX': 'doctor_syria',
    'VERSION': 1,
    'TIMEOUT': 300,  # seconds
}

# Email Security Configuration
EMAIL_SECURITY = {
    'USE_TLS': True,
    'REQUIRE_VERIFICATION': True,
    'VERIFICATION_EXPIRY': timedelta(days=1),
    'MAX_DAILY_EMAILS': 100,
}

# Authentication Security Configuration
AUTH_SECURITY = {
    'LOCKOUT_DURATION': timedelta(minutes=30),
    'MAX_LOGIN_ATTEMPTS': 5,
    'REQUIRE_2FA': True,
    'REMEMBER_ME_DURATION': timedelta(days=30),
    'SESSION_EXPIRY': timedelta(hours=12),
}

# CORS Configuration
CORS_SECURITY = {
    'ALLOWED_ORIGINS': [
        'https://doctor-syria.com',
        'https://api.doctor-syria.com',
    ],
    'ALLOWED_METHODS': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    'ALLOW_CREDENTIALS': True,
    'EXPOSE_HEADERS': ['Content-Type', 'X-CSRFToken'],
}

# Rate Limiting Configuration
RATE_LIMITING = {
    'ANON_THROTTLE_RATE': '100/day',
    'USER_THROTTLE_RATE': '1000/day',
    'BURST_THROTTLE_RATE': '60/minute',
}

# Security Monitoring Configuration
SECURITY_MONITORING = {
    'ENABLE_AUDIT_LOG': True,
    'LOG_LEVEL': 'INFO',
    'ALERT_ADMINS': True,
    'ALERT_THRESHOLD': {
        'LOGIN_FAILURES': 10,
        'API_ERRORS': 100,
        'SECURITY_VIOLATIONS': 5,
    },
}
