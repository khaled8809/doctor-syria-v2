from functools import wraps

from django.core.cache import cache

from .cache_manager import CacheManager


def cache_response(timeout=None, key_prefix="view"):
    """
    مزخرف لتخزين استجابات API مؤقتًا

    مثال الاستخدام:
    @cache_response(timeout=3600, key_prefix='user_profile')
    def get_user_profile(request, user_id):
        ...
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # توليد مفتاح فريد بناءً على المسار والمعلمات
            cache_key = CacheManager.generate_key(
                key_prefix, request.path, request.GET.dict(), *args, **kwargs
            )

            # محاولة استرجاع النتيجة من الذاكرة المؤقتة
            response = cache.get(cache_key)

            if response is None:
                # إذا لم تكن النتيجة موجودة، قم بتنفيذ الدالة وتخزين النتيجة
                response = view_func(request, *args, **kwargs)
                cache.set(cache_key, response, timeout)

            return response

        return _wrapped_view

    return decorator


def cache_method(timeout=None):
    """
    مزخرف لتخزين نتائج طرق النموذج مؤقتًا

    مثال الاستخدام:
    @cache_method(timeout=3600)
    def get_total_appointments(self):
        ...
    """

    def decorator(method):
        @wraps(method)
        def _wrapped_method(self, *args, **kwargs):
            # توليد مفتاح فريد بناءً على اسم الصنف والطريقة والمعلمات
            cache_key = CacheManager.generate_key(
                self.__class__.__name__, method.__name__, self.id, *args, **kwargs
            )

            return CacheManager.get_or_set(
                cache_key, lambda: method(self, *args, **kwargs), timeout
            )

        return _wrapped_method

    return decorator


def invalidate_cache_on_save(sender, key_prefix=None):
    """
    مزخرف لإبطال التخزين المؤقت عند حفظ النموذج

    مثال الاستخدام:
    @invalidate_cache_on_save(sender=User, key_prefix='user_profile')
    def save(self, *args, **kwargs):
        ...
    """

    def decorator(save_method):
        @wraps(save_method)
        def _wrapped_save(self, *args, **kwargs):
            # تنفيذ طريقة الحفظ الأصلية
            result = save_method(self, *args, **kwargs)

            # إبطال التخزين المؤقت
            if key_prefix:
                pattern = f"{key_prefix}:{self.id}"
                CacheManager.invalidate_pattern(pattern)

            return result

        return _wrapped_save

    return decorator
