from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone

class Appointment(models.Model):
    """نموذج المواعيد"""
    
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('cancelled', _('Cancelled')),
        ('completed', _('Completed')),
    ]
    
    PRIORITY_CHOICES = [
        ('normal', _('Normal')),
        ('urgent', _('Urgent')),
        ('emergency', _('Emergency')),
    ]

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_appointments',
        verbose_name=_('Patient')
    )
    
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_appointments',
        verbose_name=_('Doctor')
    )
    
    appointment_date = models.DateTimeField(
        verbose_name=_('Appointment Date')
    )
    
    reason = models.TextField(
        verbose_name=_('Reason for Visit')
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Status')
    )
    
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='normal',
        verbose_name=_('Priority')
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notes')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )
    
    reminder_sent = models.BooleanField(
        default=False,
        verbose_name=_('Reminder Sent')
    )

    class Meta:
        verbose_name = _('Appointment')
        verbose_name_plural = _('Appointments')
        ordering = ['-appointment_date']

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.appointment_date}"

    def clean(self):
        """التحقق من صحة البيانات"""
        if self.appointment_date < timezone.now():
            raise ValidationError(_('Appointment date cannot be in the past'))

        # التحقق من عدم وجود تعارض في المواعيد
        conflicting_appointments = Appointment.objects.filter(
            doctor=self.doctor,
            appointment_date__year=self.appointment_date.year,
            appointment_date__month=self.appointment_date.month,
            appointment_date__day=self.appointment_date.day,
            appointment_date__hour=self.appointment_date.hour,
            status__in=['pending', 'confirmed']
        ).exclude(pk=self.pk)

        if conflicting_appointments.exists():
            raise ValidationError(_('Doctor already has an appointment at this time'))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class WaitingList(models.Model):
    """نموذج قائمة الانتظار"""
    
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='waiting_list_entries',
        verbose_name=_('Patient')
    )
    
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_waiting_list',
        verbose_name=_('Doctor')
    )
    
    reason = models.TextField(
        verbose_name=_('Reason for Visit')
    )
    
    priority = models.CharField(
        max_length=20,
        choices=Appointment.PRIORITY_CHOICES,
        default='normal',
        verbose_name=_('Priority')
    )
    
    preferred_date = models.DateField(
        verbose_name=_('Preferred Date'),
        help_text=_('Preferred date for the appointment')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notes')
    )
    
    is_processed = models.BooleanField(
        default=False,
        verbose_name=_('Is Processed')
    )

    class Meta:
        verbose_name = _('Waiting List Entry')
        verbose_name_plural = _('Waiting List Entries')
        ordering = ['priority', 'created_at']

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.preferred_date}"


class Schedule(models.Model):
    """نموذج جدول الدوام"""
    
    DAYS_OF_WEEK = [
        (0, _('Monday')),
        (1, _('Tuesday')),
        (2, _('Wednesday')),
        (3, _('Thursday')),
        (4, _('Friday')),
        (5, _('Saturday')),
        (6, _('Sunday')),
    ]
    
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name=_('Doctor')
    )
    
    day_of_week = models.IntegerField(
        choices=DAYS_OF_WEEK,
        verbose_name=_('Day of Week')
    )
    
    start_time = models.TimeField(
        verbose_name=_('Start Time')
    )
    
    end_time = models.TimeField(
        verbose_name=_('End Time')
    )
    
    break_start = models.TimeField(
        null=True,
        blank=True,
        verbose_name=_('Break Start Time')
    )
    
    break_end = models.TimeField(
        null=True,
        blank=True,
        verbose_name=_('Break End Time')
    )
    
    appointment_duration = models.IntegerField(
        default=30,
        help_text=_('Duration of each appointment in minutes'),
        verbose_name=_('Appointment Duration')
    )
    
    is_available = models.BooleanField(
        default=True,
        verbose_name=_('Is Available')
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notes')
    )
    
    class Meta:
        verbose_name = _('Schedule')
        verbose_name_plural = _('Schedules')
        ordering = ['day_of_week', 'start_time']
        unique_together = ['doctor', 'day_of_week']
    
    def __str__(self):
        return f"{self.doctor} - {self.get_day_of_week_display()}"
    
    def clean(self):
        """التحقق من صحة البيانات"""
        if self.start_time >= self.end_time:
            raise ValidationError(_('End time must be after start time'))
        
        if self.break_start and self.break_end:
            if self.break_start >= self.break_end:
                raise ValidationError(_('Break end time must be after break start time'))
            
            if self.break_start < self.start_time or self.break_end > self.end_time:
                raise ValidationError(_('Break time must be within working hours'))
    
    def get_available_slots(self, date):
        """الحصول على المواعيد المتاحة في تاريخ معين"""
        from datetime import datetime, timedelta
        
        if date.weekday() != self.day_of_week:
            return []
        
        slots = []
        current_time = datetime.combine(date, self.start_time)
        end_time = datetime.combine(date, self.end_time)
        
        while current_time + timedelta(minutes=self.appointment_duration) <= end_time:
            # تخطي وقت الاستراحة
            if self.break_start and self.break_end:
                break_start = datetime.combine(date, self.break_start)
                break_end = datetime.combine(date, self.break_end)
                if break_start <= current_time <= break_end:
                    current_time = break_end
                    continue
            
            # التحقق من عدم وجود موعد محجوز
            appointment_exists = Appointment.objects.filter(
                doctor=self.doctor,
                appointment_date=current_time,
                status__in=['pending', 'confirmed']
            ).exists()
            
            if not appointment_exists:
                slots.append(current_time.time())
            
            current_time += timedelta(minutes=self.appointment_duration)
        
        return slots
