"""
Helper functions for security features in Doctor Syria Platform.
"""

from typing import Optional, Dict, Any
from django.http import HttpRequest, HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.conf import settings

from .password_validation import validate_password, get_password_strength
from .upload_handlers import SecureFileUploadHandler


def secure_upload_file(request: HttpRequest, file_field: str) -> Dict[str, Any]:
    """
    Securely handle file upload with comprehensive validation.
    
    Args:
        request: The HTTP request containing the file
        file_field: Name of the file field in request.FILES
    
    Returns:
        dict: Information about the uploaded file
        
    Raises:
        ValidationError: If file is invalid or potentially dangerous
    """
    if file_field not in request.FILES:
        raise ValidationError("No file was uploaded")
    
    uploaded_file = request.FILES[file_field]
    handler = SecureFileUploadHandler()
    
    try:
        handler.handle_uploaded_file(uploaded_file)
        return {
            'name': uploaded_file.name,
            'size': uploaded_file.size,
            'content_type': uploaded_file.content_type,
            'is_secure': True
        }
    except ValidationError as e:
        raise ValidationError(f"File validation failed: {str(e)}")


def validate_user_password(password: str, user_id: Optional[int] = None) -> Dict[str, Any]:
    """
    Validate user password and provide comprehensive feedback.
    
    Args:
        password: The password to validate
        user_id: Optional user ID to check password history
    
    Returns:
        dict: Password validation results and strength information
    """
    try:
        # Validate password
        validate_password(password)
        
        # Get password strength
        strength_info = get_password_strength(password)
        
        # Check password history if user_id provided
        history_check = True
        if user_id:
            User = get_user_model()
            try:
                user = User.objects.get(id=user_id)
                if hasattr(user, 'password_history'):
                    for old_password in user.password_history.all():
                        if old_password.check_password(password):
                            history_check = False
                            break
            except User.DoesNotExist:
                pass
        
        return {
            'is_valid': True,
            'strength_score': strength_info['score'],
            'strength_level': strength_info['strength'],
            'feedback': strength_info['feedback'],
            'passes_history': history_check
        }
    
    except ValidationError as e:
        return {
            'is_valid': False,
            'errors': [str(error) for error in e.error_list],
            'strength_score': 0,
            'strength_level': 'weak',
            'passes_history': False
        }


def add_security_headers(response: HttpResponse) -> HttpResponse:
    """
    Add security headers to HTTP response.
    
    Args:
        response: The HTTP response object
    
    Returns:
        HttpResponse: Response with added security headers
    """
    security_headers = getattr(settings, 'SECURITY_HEADERS', {})
    
    for header, value in security_headers.items():
        if header not in response:
            response[header] = value
    
    return response


def get_client_ip(request: HttpRequest) -> str:
    """
    Get client IP address from request, handling proxy servers.
    
    Args:
        request: The HTTP request
    
    Returns:
        str: Client IP address
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_request_rate(request: HttpRequest, key_prefix: str) -> bool:
    """
    Check if request exceeds rate limits.
    
    Args:
        request: The HTTP request
        key_prefix: Prefix for rate limiting key
    
    Returns:
        bool: True if request is allowed, False if rate limit exceeded
    """
    from django.core.cache import cache
    
    client_ip = get_client_ip(request)
    cache_key = f"rate_limit:{key_prefix}:{client_ip}"
    
    # Get rate limit settings
    rate_limits = getattr(settings, 'RATE_LIMITING', {})
    max_requests = rate_limits.get(f'{key_prefix.upper()}_THROTTLE_RATE', '100/day')
    count, period = max_requests.split('/')
    
    try:
        current = cache.get(cache_key, 0)
        if current >= int(count):
            return False
        
        cache.incr(cache_key)
        if current == 0:
            if period == 'minute':
                cache.expire(cache_key, 60)
            elif period == 'hour':
                cache.expire(cache_key, 3600)
            elif period == 'day':
                cache.expire(cache_key, 86400)
        
        return True
    
    except Exception:
        # If cache fails, allow request but log error
        return True
