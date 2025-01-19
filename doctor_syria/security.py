"""
إعدادات الأمان
Security Settings

This module contains security-related settings and utilities for the Doctor Syria project.
"""

import logging
from typing import Any, Dict, List

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest

# تكوين التسجيل | Configure logging
logger = logging.getLogger("security")

# إعدادات كلمة المرور | Password settings
PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 10,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# إعدادات الجلسة | Session settings
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Strict"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600  # 1 hour

# إعدادات CSRF | CSRF settings
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Strict"
CSRF_TRUSTED_ORIGINS: List[str] = []

# إعدادات الأمان العامة | General security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# قائمة المضيفين المسموح بهم | Allowed hosts
ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]


def check_user_permissions(user: Any, required_permissions: List[str]) -> bool:
    """
    التحقق من صلاحيات المستخدم
    Check if user has required permissions

    Args:
        user: المستخدم | User object
        required_permissions: الصلاحيات المطلوبة | List of required permissions

    Returns:
        bool: True if user has all required permissions
    """
    if user.is_superuser:
        return True
    return all(user.has_perm(perm) for perm in required_permissions)


def log_security_event(
    request: HttpRequest, event_type: str, description: str, severity: str = "INFO"
) -> None:
    """
    تسجيل حدث أمني
    Log a security event

    Args:
        request: طلب HTTP | HTTP request
        event_type: نوع الحدث | Type of event
        description: وصف الحدث | Event description
        severity: مستوى الخطورة | Severity level
    """
    ip = request.META.get("REMOTE_ADDR")
    user = request.user.username if request.user.is_authenticated else "anonymous"

    log_data = {
        "ip": ip,
        "user": user,
        "event_type": event_type,
        "description": description,
        "severity": severity,
    }

    if severity == "ERROR":
        logger.error(str(log_data))
    elif severity == "WARNING":
        logger.warning(str(log_data))
    else:
        logger.info(str(log_data))


def check_rate_limit(request: HttpRequest, limit: int = 100) -> bool:
    """
    التحقق من حد معدل الطلبات
    Check if request is within rate limit

    Args:
        request: طلب HTTP | HTTP request
        limit: الحد الأقصى للطلبات | Maximum number of requests

    Returns:
        bool: True if within limit
    """
    ip = request.META.get("REMOTE_ADDR")
    key = f"rate_limit_{ip}"

    from django.core.cache import cache

    count = cache.get(key, 0)

    if count >= limit:
        log_security_event(
            request,
            "RATE_LIMIT_EXCEEDED",
            f"Rate limit exceeded for IP {ip}",
            "WARNING",
        )
        return False

    cache.set(key, count + 1, 3600)  # 1 hour expiry
    return True


def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    تنظيف البيانات المدخلة
    Sanitize input data

    Args:
        data: البيانات المدخلة | Input data

    Returns:
        Dict: Sanitized data
    """
    import bleach

    def clean_value(value: Any) -> Any:
        if isinstance(value, str):
            return bleach.clean(
                value, tags=["p", "b", "i", "u"], attributes={}, strip=True
            )
        elif isinstance(value, dict):
            return {k: clean_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [clean_value(item) for item in value]
        return value

    return {k: clean_value(v) for k, v in data.items()}


def encrypt_sensitive_data(data: str) -> str:
    """
    تشفير البيانات الحساسة
    Encrypt sensitive data

    Args:
        data: البيانات | Data to encrypt

    Returns:
        str: Encrypted data
    """
    from cryptography.fernet import Fernet

    key = settings.ENCRYPTION_KEY
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()


def decrypt_sensitive_data(encrypted_data: str) -> str:
    """
    فك تشفير البيانات الحساسة
    Decrypt sensitive data

    Args:
        encrypted_data: البيانات المشفرة | Encrypted data

    Returns:
        str: Decrypted data
    """
    from cryptography.fernet import Fernet

    key = settings.ENCRYPTION_KEY
    f = Fernet(key)
    return f.decrypt(encrypted_data.encode()).decode()


class SecurityMiddleware:
    """
    وسيط الأمان
    Security middleware for request/response processing
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> Any:
        # التحقق من حد معدل الطلبات | Check rate limit
        if not check_rate_limit(request):
            raise PermissionDenied("Too many requests")

        # تنظيف البيانات المدخلة | Clean input data
        if request.method in ["POST", "PUT", "PATCH"]:
            request.POST = sanitize_input(request.POST.dict())

        response = self.get_response(request)

        # إضافة رؤوس الأمان | Add security headers
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["X-XSS-Protection"] = "1; mode=block"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response["Permissions-Policy"] = "geolocation=(), microphone=()"

        return response
