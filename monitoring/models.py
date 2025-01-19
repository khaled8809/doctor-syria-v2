"""
نماذج نظام المراقبة والتتبع
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class SystemMetric(models.Model):
    """نموذج لتخزين مقاييس النظام"""

    METRIC_TYPES = (
        ("cpu", "استخدام المعالج"),
        ("memory", "استخدام الذاكرة"),
        ("disk", "استخدام القرص"),
        ("response_time", "زمن الاستجابة"),
        ("error_rate", "معدل الأخطاء"),
        ("request_rate", "معدل الطلبات"),
    )

    metric_type = models.CharField(
        max_length=20, choices=METRIC_TYPES, verbose_name=_("نوع المقياس")
    )
    value = models.FloatField(verbose_name=_("القيمة"))
    timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name=_("وقت التسجيل"), db_index=True
    )

    class Meta:
        verbose_name = _("مقياس النظام")
        verbose_name_plural = _("مقاييس النظام")
        indexes = [
            models.Index(fields=["metric_type", "timestamp"]),
        ]


class ErrorLog(models.Model):
    """نموذج لتسجيل الأخطاء"""

    SEVERITY_LEVELS = (
        ("critical", "حرج"),
        ("error", "خطأ"),
        ("warning", "تحذير"),
        ("info", "معلومة"),
    )

    message = models.TextField(verbose_name=_("رسالة الخطأ"))
    severity = models.CharField(
        max_length=10, choices=SEVERITY_LEVELS, verbose_name=_("مستوى الخطورة")
    )
    source = models.CharField(max_length=255, verbose_name=_("مصدر الخطأ"))
    stack_trace = models.TextField(blank=True, null=True, verbose_name=_("تتبع المكدس"))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("المستخدم"),
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name=_("وقت التسجيل"), db_index=True
    )

    class Meta:
        verbose_name = _("سجل الأخطاء")
        verbose_name_plural = _("سجلات الأخطاء")
        indexes = [
            models.Index(fields=["severity", "timestamp"]),
            models.Index(fields=["source", "timestamp"]),
        ]


class PerformanceLog(models.Model):
    """نموذج لتسجيل أداء النظام"""

    endpoint = models.CharField(max_length=255, verbose_name=_("نقطة النهاية"))
    method = models.CharField(max_length=10, verbose_name=_("الطريقة"))
    response_time = models.FloatField(verbose_name=_("زمن الاستجابة"))
    status_code = models.IntegerField(verbose_name=_("رمز الحالة"))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("المستخدم"),
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name=_("وقت التسجيل"), db_index=True
    )

    class Meta:
        verbose_name = _("سجل الأداء")
        verbose_name_plural = _("سجلات الأداء")
        indexes = [
            models.Index(fields=["endpoint", "timestamp"]),
            models.Index(fields=["status_code", "timestamp"]),
        ]
