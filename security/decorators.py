from functools import wraps

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.utils.translation import gettext as _


def role_required(roles):
    """التحقق من دور المستخدم"""

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden(_("يجب تسجيل الدخول"))

            if not isinstance(roles, (list, tuple)):
                roles_list = [roles]
            else:
                roles_list = roles

            if request.user.role not in roles_list:
                raise PermissionDenied(_("ليس لديك صلاحية للوصول"))

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def permission_required(permissions):
    """التحقق من صلاحيات المستخدم"""

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden(_("يجب تسجيل الدخول"))

            if not isinstance(permissions, (list, tuple)):
                permissions_list = [permissions]
            else:
                permissions_list = permissions

            user_permissions = request.user.get_role_permissions()
            if "all" not in user_permissions:
                if not any(perm in user_permissions for perm in permissions_list):
                    raise PermissionDenied(_("ليس لديك الصلاحيات المطلوبة"))

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def require_https(view_func):
    """إجبار استخدام HTTPS"""

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.is_secure():
            return HttpResponseForbidden(_("يجب استخدام HTTPS"))
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def audit_log(action):
    """تسجيل العمليات"""

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)

            from security.models import AuditLog

            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                action=action,
                ip_address=request.META.get("REMOTE_ADDR"),
                user_agent=request.META.get("HTTP_USER_AGENT"),
                path=request.path,
                method=request.method,
                status_code=response.status_code,
            )

            return response

        return _wrapped_view

    return decorator
