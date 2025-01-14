import logging
import re
from datetime import timedelta
from typing import Optional

from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.utils import timezone

logger = logging.getLogger(__name__)


class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # تجميع التعبيرات النمطية للمسارات المستثناة
        self.exempt_urls = [re.compile(url) for url in settings.SECURITY_EXEMPT_URLS]

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # فحص الأمان قبل معالجة الطلب
        if not self.is_path_exempt(request.path):
            # فحص معدل الطلبات
            if not self.check_rate_limit(request):
                return HttpResponse("تم تجاوز الحد المسموح من الطلبات", status=429)

            # فحص محاولات الاختراق
            if self.detect_security_threats(request):
                self.log_security_threat(request)
                return HttpResponse("تم اكتشاف تهديد أمني محتمل", status=403)

            # فحص صحة الجلسة
            if not self.validate_session(request):
                return HttpResponse("جلسة غير صالحة", status=401)

        response = self.get_response(request)

        # إضافة رؤوس الأمان
        self.add_security_headers(response)

        return response

    def is_path_exempt(self, path: str) -> bool:
        """التحقق مما إذا كان المسار معفى من فحوصات الأمان"""
        return any(pattern.match(path) for pattern in self.exempt_urls)

    def check_rate_limit(self, request: HttpRequest) -> bool:
        """التحقق من معدل الطلبات"""
        client_ip = self.get_client_ip(request)
        cache_key = f"rate_limit_{client_ip}"

        requests = cache.get(cache_key, 0)
        if requests >= settings.RATE_LIMIT_MAX_REQUESTS:
            return False

        cache.set(cache_key, requests + 1, settings.RATE_LIMIT_PERIOD)
        return True

    def detect_security_threats(self, request: HttpRequest) -> bool:
        """اكتشاف التهديدات الأمنية المحتملة"""
        # فحص محاولات SQL Injection
        if self.detect_sql_injection(request):
            return True

        # فحص محاولات XSS
        if self.detect_xss(request):
            return True

        # فحص محاولات Path Traversal
        if self.detect_path_traversal(request):
            return True

        return False

    def detect_sql_injection(self, request: HttpRequest) -> bool:
        """اكتشاف محاولات SQL Injection"""
        sql_patterns = [
            r"(\s|^)(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER)(\s|$)",
            r"--",
            r";.*?$",
            r"/\*.*?\*/",
        ]

        for pattern in sql_patterns:
            if self.check_pattern_in_request(request, pattern):
                return True
        return False

    def detect_xss(self, request: HttpRequest) -> bool:
        """اكتشاف محاولات XSS"""
        xss_patterns = [
            r"<script.*?>",
            r"javascript:",
            r"onerror=",
            r"onload=",
            r"eval\(",
            r"document\.",
        ]

        for pattern in xss_patterns:
            if self.check_pattern_in_request(request, pattern):
                return True
        return False

    def detect_path_traversal(self, request: HttpRequest) -> bool:
        """اكتشاف محاولات Path Traversal"""
        path_patterns = [r"\.\.", r"%2e%2e", r"\.\./", r"/etc/passwd"]

        for pattern in path_patterns:
            if self.check_pattern_in_request(request, pattern):
                return True
        return False

    def check_pattern_in_request(self, request: HttpRequest, pattern: str) -> bool:
        """فحص وجود نمط في الطلب"""
        # فحص المسار
        if re.search(pattern, request.path, re.I):
            return True

        # فحص معلمات GET
        for key, value in request.GET.items():
            if re.search(pattern, str(value), re.I):
                return True

        # فحص معلمات POST
        for key, value in request.POST.items():
            if re.search(pattern, str(value), re.I):
                return True

        return False

    def validate_session(self, request: HttpRequest) -> bool:
        """التحقق من صحة الجلسة"""
        if not request.user.is_authenticated:
            return True

        session = request.session
        if not session.get("last_activity"):
            return False

        last_activity = session["last_activity"]
        if timezone.now() - last_activity > timedelta(
            minutes=settings.SESSION_IDLE_TIMEOUT
        ):
            return False

        session["last_activity"] = timezone.now()
        return True

    def add_security_headers(self, response: HttpResponse) -> None:
        """إضافة رؤوس الأمان"""
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["X-XSS-Protection"] = "1; mode=block"
        response["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response["Content-Security-Policy"] = "default-src 'self'"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response["Feature-Policy"] = "geolocation 'none'"

    def get_client_ip(self, request: HttpRequest) -> Optional[str]:
        """الحصول على عنوان IP للعميل"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")

    def log_security_threat(self, request: HttpRequest) -> None:
        """تسجيل التهديد الأمني"""
        logger.warning(
            "تم اكتشاف تهديد أمني محتمل",
            extra={
                "path": request.path,
                "method": request.method,
                "ip": self.get_client_ip(request),
                "user": (
                    request.user.username
                    if request.user.is_authenticated
                    else "anonymous"
                ),
                "data": {
                    "GET": dict(request.GET),
                    "POST": dict(request.POST),
                    "headers": dict(request.headers),
                },
            },
        )
