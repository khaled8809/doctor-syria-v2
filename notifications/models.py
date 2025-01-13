"""
نماذج نظام الإشعارات
"""

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    """نموذج الإشعارات الأساسي"""

    NOTIFICATION_TYPES = (
        ("appointment", "موعد"),
        ("medical", "طبي"),
        ("system", "نظام"),
        ("message", "رسالة"),
        ("reminder", "تذكير"),
        ("alert", "تنبيه"),
    )

    PRIORITY_LEVELS = (
        ("low", "منخفض"),
        ("normal", "عادي"),
        ("high", "مرتفع"),
        ("urgent", "عاجل"),
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("المستلم"),
    )
    notification_type = models.CharField(
        max_length=20, choices=NOTIFICATION_TYPES, verbose_name=_("نوع الإشعار")
    )
    title = models.CharField(max_length=255, verbose_name=_("العنوان"))
    message = models.TextField(verbose_name=_("الرسالة"))
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_LEVELS,
        default="normal",
        verbose_name=_("الأولوية"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("تاريخ الإنشاء")
    )
    read_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_("تاريخ القراءة")
    )
    is_read = models.BooleanField(default=False, verbose_name=_("مقروء"))

    # للربط مع أي نموذج آخر
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey("content_type", "object_id")

    # بيانات إضافية
    metadata = models.JSONField(
        default=dict, blank=True, verbose_name=_("بيانات إضافية")
    )

    class Meta:
        verbose_name = _("إشعار")
        verbose_name_plural = _("إشعارات")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["recipient", "-created_at"]),
            models.Index(fields=["notification_type", "-created_at"]),
            models.Index(fields=["is_read", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.title}"

    def mark_as_read(self):
        """تحديد الإشعار كمقروء"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


class NotificationPreference(models.Model):
    """تفضيلات الإشعارات للمستخدم"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_preferences",
        verbose_name=_("المستخدم"),
    )

    # تفضيلات عامة
    email_notifications = models.BooleanField(
        default=True, verbose_name=_("إشعارات البريد الإلكتروني")
    )
    sms_notifications = models.BooleanField(
        default=True, verbose_name=_("إشعارات الرسائل النصية")
    )
    push_notifications = models.BooleanField(
        default=True, verbose_name=_("إشعارات الويب")
    )

    # تفضيلات حسب النوع
    appointment_notifications = models.BooleanField(
        default=True, verbose_name=_("إشعارات المواعيد")
    )
    medical_notifications = models.BooleanField(
        default=True, verbose_name=_("إشعارات طبية")
    )
    system_notifications = models.BooleanField(
        default=True, verbose_name=_("إشعارات النظام")
    )

    # تفضيلات متقدمة
    quiet_hours_start = models.TimeField(
        null=True, blank=True, verbose_name=_("بداية ساعات الهدوء")
    )
    quiet_hours_end = models.TimeField(
        null=True, blank=True, verbose_name=_("نهاية ساعات الهدوء")
    )
    notification_frequency = models.CharField(
        max_length=20,
        choices=[
            ("immediate", "فوري"),
            ("hourly", "كل ساعة"),
            ("daily", "يومي"),
        ],
        default="immediate",
        verbose_name=_("تكرار الإشعارات"),
    )

    class Meta:
        verbose_name = _("تفضيلات الإشعارات")
        verbose_name_plural = _("تفضيلات الإشعارات")

    def __str__(self):
        return f"تفضيلات الإشعارات - {self.user.get_full_name()}"
