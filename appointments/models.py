from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Appointment(models.Model):
    """المواعيد"""
    
    class Status(models.TextChoices):
        PENDING = 'pending', _('قيد الانتظار')
        CONFIRMED = 'confirmed', _('مؤكد')
        COMPLETED = 'completed', _('مكتمل')
        CANCELLED = 'cancelled', _('ملغي')
        RESCHEDULED = 'rescheduled', _('معاد جدولته')
    
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_appointments',
        verbose_name=_('المريض')
    )
    
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_appointments',
        verbose_name=_('الطبيب')
    )
    
    date = models.DateField(
        verbose_name=_('التاريخ')
    )
    
    time = models.TimeField(
        verbose_name=_('الوقت')
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_('الحالة')
    )
    
    reason = models.TextField(
        verbose_name=_('سبب الزيارة')
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name=_('ملاحظات')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('تاريخ التحديث')
    )
    
    cancelled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cancelled_appointments',
        verbose_name=_('ألغي بواسطة')
    )
    
    cancellation_reason = models.TextField(
        blank=True,
        verbose_name=_('سبب الإلغاء')
    )
    
    reminder_sent = models.BooleanField(
        default=False,
        verbose_name=_('تم إرسال التذكير')
    )
    
    class Meta:
        verbose_name = _('موعد')
        verbose_name_plural = _('المواعيد')
        ordering = ['date', 'time']
        
    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.date} {self.time}"
    
    def save(self, *args, **kwargs):
        """حفظ الموعد مع إرسال الإشعارات"""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            from notifications.models import Notification
            # إشعار للمريض
            Notification.objects.create(
                user=self.patient,
                title=_('تم إنشاء موعد جديد'),
                message=_(f'تم حجز موعد مع الدكتور {self.doctor.get_full_name()} '
                         f'في {self.date} الساعة {self.time}')
            )
            # إشعار للطبيب
            Notification.objects.create(
                user=self.doctor,
                title=_('موعد جديد'),
                message=_(f'لديك موعد جديد مع {self.patient.get_full_name()} '
                         f'في {self.date} الساعة {self.time}')
            )

class Schedule(models.Model):
    """جدول الدوام"""
    
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name=_('الطبيب')
    )
    
    day_of_week = models.IntegerField(
        choices=[
            (0, _('الاثنين')),
            (1, _('الثلاثاء')),
            (2, _('الأربعاء')),
            (3, _('الخميس')),
            (4, _('الجمعة')),
            (5, _('السبت')),
            (6, _('الأحد')),
        ],
        verbose_name=_('يوم الأسبوع')
    )
    
    start_time = models.TimeField(
        verbose_name=_('وقت البدء')
    )
    
    end_time = models.TimeField(
        verbose_name=_('وقت الانتهاء')
    )
    
    is_available = models.BooleanField(
        default=True,
        verbose_name=_('متاح')
    )
    
    class Meta:
        verbose_name = _('جدول')
        verbose_name_plural = _('الجداول')
        ordering = ['day_of_week', 'start_time']
        unique_together = ['doctor', 'day_of_week']
