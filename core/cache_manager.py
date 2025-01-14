import hashlib
import json
from datetime import timedelta

from django.conf import settings
from django.core.cache import cache


class CacheManager:
    """مدير التخزين المؤقت للتطبيق"""

    @staticmethod
    def generate_key(prefix, *args, **kwargs):
        """توليد مفتاح فريد للتخزين المؤقت"""
        key_parts = [prefix]
        key_parts.extend([str(arg) for arg in args])
        if kwargs:
            key_parts.append(json.dumps(kwargs, sort_keys=True))
        key_string = ":".join(key_parts)
        return f"doctor_syria:{hashlib.md5(key_string.encode()).hexdigest()}"

    @staticmethod
    def get_or_set(key, callback, timeout=None):
        """الحصول على القيمة من الذاكرة المؤقتة أو تعيينها إذا لم تكن موجودة"""
        result = cache.get(key)
        if result is None:
            result = callback()
            cache.set(key, result, timeout=timeout)
        return result

    @staticmethod
    def invalidate(key):
        """إزالة قيمة من الذاكرة المؤقتة"""
        cache.delete(key)

    @staticmethod
    def invalidate_pattern(pattern):
        """إزالة كل القيم التي تطابق نمطاً معيناً"""
        if hasattr(cache, "delete_pattern"):
            cache.delete_pattern(f"*{pattern}*")

    # مدة التخزين المؤقت الافتراضية للأنواع المختلفة من البيانات
    CACHE_TIMES = {
        "medical_record": timedelta(hours=1),
        "appointment": timedelta(minutes=15),
        "user_profile": timedelta(hours=24),
        "hospital_info": timedelta(days=1),
        "analytics": timedelta(hours=6),
    }

    @classmethod
    def cache_medical_record(cls, record_id):
        """تخزين مؤقت للسجل الطبي"""
        key = cls.generate_key("medical_record", record_id)
        return key, cls.CACHE_TIMES["medical_record"]

    @classmethod
    def cache_appointment(cls, appointment_id):
        """تخزين مؤقت للموعد"""
        key = cls.generate_key("appointment", appointment_id)
        return key, cls.CACHE_TIMES["appointment"]

    @classmethod
    def cache_user_profile(cls, user_id):
        """تخزين مؤقت لملف المستخدم"""
        key = cls.generate_key("user_profile", user_id)
        return key, cls.CACHE_TIMES["user_profile"]

    @classmethod
    def cache_hospital_info(cls, hospital_id):
        """تخزين مؤقت لمعلومات المستشفى"""
        key = cls.generate_key("hospital_info", hospital_id)
        return key, cls.CACHE_TIMES["hospital_info"]

    @classmethod
    def cache_analytics(cls, report_type, **params):
        """تخزين مؤقت للتحليلات"""
        key = cls.generate_key("analytics", report_type, **params)
        return key, cls.CACHE_TIMES["analytics"]
