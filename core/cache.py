import hashlib
import json
from functools import wraps

from django.conf import settings
from django.core.cache import cache


def cache_key_generator(*args, **kwargs):
    """توليد مفتاح للتخزين المؤقت"""
    key_parts = list(args)
    key_parts.extend(sorted(kwargs.items()))
    key = hashlib.md5(json.dumps(key_parts).encode()).hexdigest()
    return key


def cache_response(timeout=300, key_prefix="view"):
    """مخزن مؤقت للاستجابات"""

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.method != "GET":
                return view_func(request, *args, **kwargs)

            # توليد مفتاح فريد
            cache_key = (
                f"{key_prefix}:{request.path}:{cache_key_generator(args, kwargs)}"
            )

            # محاولة استرجاع النتيجة من المخزن المؤقت
            response = cache.get(cache_key)
            if response is not None:
                return response

            # تنفيذ الدالة وتخزين النتيجة
            response = view_func(request, *args, **kwargs)
            cache.set(cache_key, response, timeout)

            return response

        return _wrapped_view

    return decorator


def cache_queryset(timeout=300, key_prefix="queryset"):
    """مخزن مؤقت لنتائج الاستعلامات"""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            cache_key = (
                f"{key_prefix}:{func.__name__}:{cache_key_generator(args, kwargs)}"
            )

            result = cache.get(cache_key)
            if result is not None:
                return result

            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout)

            return result

        return _wrapped_func

    return decorator


class QuerySetCacheMixin:
    """Mixin لتخزين نتائج الاستعلامات مؤقتاً"""

    def get_cache_key(self):
        """توليد مفتاح للتخزين المؤقت"""
        return f"queryset:{self.__class__.__name__}:{self.pk}"

    def get_cache_timeout(self):
        """الحصول على مدة التخزين المؤقت"""
        return getattr(settings, "QUERYSET_CACHE_TIMEOUT", 300)

    def save(self, *args, **kwargs):
        """حفظ النموذج ومسح التخزين المؤقت"""
        cache.delete(self.get_cache_key())
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """حذف النموذج ومسح التخزين المؤقت"""
        cache.delete(self.get_cache_key())
        super().delete(*args, **kwargs)


class CacheManager:
    """مدير التخزين المؤقت"""

    @staticmethod
    def invalidate_model_cache(model_class, pk=None):
        """إبطال التخزين المؤقت لنموذج معين"""
        if pk:
            cache_key = f"queryset:{model_class.__name__}:{pk}"
            cache.delete(cache_key)
        else:
            cache.delete_pattern(f"queryset:{model_class.__name__}:*")

    @staticmethod
    def invalidate_view_cache(path_pattern="*"):
        """إبطال التخزين المؤقت لمسار معين"""
        cache.delete_pattern(f"view:{path_pattern}")

    @staticmethod
    def warm_up_cache(queryset, timeout=300):
        """تحميل مسبق للتخزين المؤقت"""
        for obj in queryset:
            cache_key = f"queryset:{obj.__class__.__name__}:{obj.pk}"
            cache.set(cache_key, obj, timeout)
