"""
نماذج نظام النسخ الاحتياطي
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
import os

class BackupJob(models.Model):
    """نموذج لتخزين معلومات مهام النسخ الاحتياطي"""
    
    BACKUP_TYPES = (
        ('full', 'نسخة كاملة'),
        ('incremental', 'نسخة تزايدية'),
        ('differential', 'نسخة تفاضلية'),
    )

    STATUS_CHOICES = (
        ('pending', 'قيد الانتظار'),
        ('running', 'قيد التنفيذ'),
        ('completed', 'مكتمل'),
        ('failed', 'فشل'),
    )

    backup_type = models.CharField(
        max_length=20,
        choices=BACKUP_TYPES,
        verbose_name=_('نوع النسخ الاحتياطي')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('الحالة')
    )
    started_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('وقت البدء')
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('وقت الإكمال')
    )
    file_path = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('مسار الملف')
    )
    file_size = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name=_('حجم الملف')
    )
    error_message = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('رسالة الخطأ')
    )

    class Meta:
        verbose_name = _('مهمة نسخ احتياطي')
        verbose_name_plural = _('مهام النسخ الاحتياطي')
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.get_backup_type_display()} - {self.started_at}"

    def get_file_size_display(self):
        """عرض حجم الملف بشكل مقروء"""
        if not self.file_size:
            return "0 B"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if self.file_size < 1024:
                return f"{self.file_size:.1f} {unit}"
            self.file_size /= 1024
        return f"{self.file_size:.1f} TB"

class RestorePoint(models.Model):
    """نموذج لتخزين نقاط الاستعادة"""
    
    backup = models.ForeignKey(
        BackupJob,
        on_delete=models.CASCADE,
        related_name='restore_points',
        verbose_name=_('النسخة الاحتياطية')
    )
    description = models.TextField(
        verbose_name=_('الوصف')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء')
    )
    is_automated = models.BooleanField(
        default=False,
        verbose_name=_('تلقائي')
    )
    metadata = models.JSONField(
        default=dict,
        verbose_name=_('البيانات الوصفية')
    )

    class Meta:
        verbose_name = _('نقطة استعادة')
        verbose_name_plural = _('نقاط الاستعادة')
        ordering = ['-created_at']

    def __str__(self):
        return f"نقطة استعادة - {self.created_at}"
