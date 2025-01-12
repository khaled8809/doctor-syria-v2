from django.conf import settings
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
import re

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Check for basic security headers
        self.check_security_headers(request)
        
        # Check for suspicious patterns
        if self.contains_suspicious_patterns(request):
            return HttpResponseForbidden("Suspicious request pattern detected")
            
        # Add security headers to response
        response = self.get_response(request)
        self.add_security_headers(response)
        
        return response
        
    def check_security_headers(self, request):
        # Check for required headers in production
        if not settings.DEBUG:
            required_headers = ['HTTP_X_REQUESTED_WITH', 'HTTP_REFERER']
            for header in required_headers:
                if header not in request.META:
                    raise PermissionDenied()
                    
    def contains_suspicious_patterns(self, request):
        # Check for SQL injection patterns
        sql_patterns = [
            r'(\s|^)(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER)(\s|$)',
            r'(--)(\s|$)',
            r'(;)(\s|$)'
        ]
        
        # Check for XSS patterns
        xss_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'onload=',
            r'onerror='
        ]
        
        # Combine all patterns
        patterns = sql_patterns + xss_patterns
        
        # Check request parameters
        for key, value in request.GET.items():
            for pattern in patterns:
                if re.search(pattern, value, re.IGNORECASE):
                    return True
                    
        for key, value in request.POST.items():
            for pattern in patterns:
                if re.search(pattern, value, re.IGNORECASE):
                    return True
                    
        return False
        
    def add_security_headers(self, response):
        # Add security headers
        security_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';",
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=()'
        }
        
        for header, value in security_headers.items():
            response[header] = value
