"""
Models for the notifications application.

This module defines all models related to notifications, including:
- Notification templates
- Notification preferences
- Notification channels and delivery methods
"""
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from core.models import TimestampMixin


class NotificationTemplate(TimestampMixin):
    """
    Notification templates for different types of notifications
    """
    name = models.CharField(_('الاسم'), max_length=100)
    code = models.CharField(_('الرمز'), max_length=50, unique=True)
    title_template = models.CharField(_('قالب العنوان'), max_length=200)
    body_template = models.TextField(_('قالب المحتوى'))
    category = models.CharField(
        _('الفئة'),
        max_length=50,
        choices=(
            ('appointment', _('المواعيد')),
            ('medical', _('طبي')),
            ('pharmacy', _('صيدلية')),
            ('laboratory', _('مختبر')),
            ('billing', _('فواتير')),
            ('system', _('نظام'))
        )
    )
    is_active = models.BooleanField(_('نشط'), default=True)
    
    class Meta:
        verbose_name = _('قالب إشعار')
        verbose_name_plural = _('قوالب الإشعارات')
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.category})"


class NotificationChannel(TimestampMixin):
    """
    Notification delivery channels
    """
    name = models.CharField(_('الاسم'), max_length=100)
    code = models.CharField(_('الرمز'), max_length=50, unique=True)
    description = models.TextField(_('الوصف'), blank=True)
    is_active = models.BooleanField(_('نشط'), default=True)
    icon = models.CharField(_('الأيقونة'), max_length=50, blank=True)
    config = models.JSONField(_('الإعدادات'), default=dict, blank=True)
    
    class Meta:
        verbose_name = _('قناة إشعار')
        verbose_name_plural = _('قنوات الإشعارات')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class NotificationPreference(TimestampMixin):
    """
    User notification preferences
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notification_preferences',
        verbose_name=_('المستخدم')
    )
    template = models.ForeignKey(
        NotificationTemplate,
        on_delete=models.CASCADE,
        related_name='preferences',
        verbose_name=_('القالب')
    )
    channel = models.ForeignKey(
        NotificationChannel,
        on_delete=models.CASCADE,
        related_name='preferences',
        verbose_name=_('القناة')
    )
    is_enabled = models.BooleanField(_('مفعل'), default=True)
    custom_schedule = models.JSONField(
        _('جدول مخصص'),
        default=dict,
        blank=True,
        help_text=_('توقيت مخصص لإرسال الإشعارات')
    )
    
    class Meta:
        verbose_name = _('تفضيل إشعار')
        verbose_name_plural = _('تفضيلات الإشعارات')
        unique_together = ['user', 'template', 'channel']
    
    def __str__(self):
        return f"{self.user} - {self.template} ({self.channel})"


class Notification(TimestampMixin):
    """
    Notification model for storing all notifications
    """
    STATUS_CHOICES = (
        ('pending', _('قيد الانتظار')),
        ('sent', _('تم الإرسال')),
        ('delivered', _('تم التوصيل')),
        ('read', _('تمت القراءة')),
        ('failed', _('فشل')),
    )
    
    PRIORITY_CHOICES = (
        ('low', _('منخفض')),
        ('normal', _('عادي')),
        ('high', _('مرتفع')),
        ('urgent', _('عاجل')),
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('المستخدم')
    )
    template = models.ForeignKey(
        NotificationTemplate,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('القالب')
    )
    title = models.CharField(_('العنوان'), max_length=200)
    body = models.TextField(_('المحتوى'))
    status = models.CharField(
        _('الحالة'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    priority = models.CharField(
        _('الأولوية'),
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='normal'
    )
    sent_at = models.DateTimeField(_('تاريخ الإرسال'), null=True, blank=True)
    delivered_at = models.DateTimeField(
        _('تاريخ التوصيل'),
        null=True,
        blank=True
    )
    read_at = models.DateTimeField(_('تاريخ القراءة'), null=True, blank=True)
    
    # Generic relation to the related object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Additional data for the notification
    data = models.JSONField(_('بيانات إضافية'), default=dict, blank=True)
    
    class Meta:
        verbose_name = _('إشعار')
        verbose_name_plural = _('الإشعارات')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def __str__(self):
        return f"{self.user} - {self.title}"
    
    def mark_as_sent(self):
        """تحديث حالة الإشعار إلى 'تم الإرسال'"""
        self.status = 'sent'
        self.sent_at = timezone.now()
        self.save()
    
    def mark_as_delivered(self):
        """تحديث حالة الإشعار إلى 'تم التوصيل'"""
        self.status = 'delivered'
        self.delivered_at = timezone.now()
        self.save()
    
    def mark_as_read(self):
        """تحديث حالة الإشعار إلى 'تمت القراءة'"""
        self.status = 'read'
        self.read_at = timezone.now()
        self.save()


class NotificationDelivery(TimestampMixin):
    """
    Notification delivery attempts and status
    """
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name='deliveries',
        verbose_name=_('الإشعار')
    )
    channel = models.ForeignKey(
        NotificationChannel,
        on_delete=models.CASCADE,
        related_name='deliveries',
        verbose_name=_('القناة')
    )
    status = models.CharField(
        _('الحالة'),
        max_length=20,
        choices=Notification.STATUS_CHOICES,
        default='pending'
    )
    attempt_count = models.PositiveIntegerField(_('عدد المحاولات'), default=0)
    last_attempt = models.DateTimeField(
        _('آخر محاولة'),
        null=True,
        blank=True
    )
    error_message = models.TextField(_('رسالة الخطأ'), blank=True)
    delivery_data = models.JSONField(
        _('بيانات التوصيل'),
        default=dict,
        blank=True
    )
    
    class Meta:
        verbose_name = _('توصيل إشعار')
        verbose_name_plural = _('توصيلات الإشعارات')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.notification} - {self.channel}"
