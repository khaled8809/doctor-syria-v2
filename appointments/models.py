from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ExpressionWrapper, F, FloatField
from django.db.models.functions import Now
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from patient_records.models import Patient
from doctors.models import Doctor


class Appointment(models.Model):
    """نموذج المواعيد"""

    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("confirmed", _("Confirmed")),
        ("cancelled", _("Cancelled")),
        ("completed", _("Completed")),
    ]

    PRIORITY_CHOICES = [
        ("normal", _("Normal")),
        ("urgent", _("Urgent")),
        ("emergency", _("Emergency")),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name=_("Patient"),
        db_index=True,
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name=_("Doctor"),
        db_index=True,
    )

    appointment_date = models.DateTimeField(
        verbose_name=_("Appointment Date"), db_index=True
    )

    reason = models.TextField(verbose_name=_("Reason for Visit"))

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name=_("Status"),
        db_index=True,
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="normal",
        verbose_name=_("Priority"),
    )

    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At"), db_index=True
    )

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    reminder_sent = models.BooleanField(default=False, verbose_name=_("Reminder Sent"))

    class Meta:
        verbose_name = _("Appointment")
        verbose_name_plural = _("Appointments")
        ordering = ["-appointment_date"]
        indexes = [
            models.Index(fields=["appointment_date", "status"]),
            models.Index(fields=["doctor", "appointment_date"]),
            models.Index(fields=["patient", "appointment_date"]),
        ]

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.appointment_date}"

    def clean(self):
        """التحقق من صحة البيانات"""
        super().clean()

        # التحقق من تاريخ الموعد
        if self.appointment_date < timezone.now():
            raise ValidationError(_("Appointment date cannot be in the past"))

        # التحقق من توفر الطبيب في هذا اليوم
        schedule = Schedule.objects.filter(
            doctor=self.doctor,
            day_of_week=self.appointment_date.weekday(),
            is_available=True,
        ).first()

        if not schedule:
            raise ValidationError(_("Doctor is not available on this day"))

        # التحقق من وقت الموعد ضمن ساعات العمل
        appointment_time = self.appointment_date.time()
        if (
            appointment_time < schedule.start_time
            or appointment_time > schedule.end_time
        ):
            raise ValidationError(_("Appointment time is outside working hours"))

        # التحقق من وقت الراحة
        if schedule.break_start and schedule.break_end:
            if schedule.break_start <= appointment_time <= schedule.break_end:
                raise ValidationError(_("Appointment time is during break hours"))

        # التحقق من تعارض المواعيد
        appointment_end = self.appointment_date + timezone.timedelta(
            minutes=schedule.appointment_duration
        )
        conflicting_appointments = Appointment.objects.filter(
            doctor=self.doctor,
            status__in=["pending", "confirmed"],
            appointment_date__lt=appointment_end,
            appointment_date__gt=self.appointment_date
            - timezone.timedelta(minutes=schedule.appointment_duration),
        ).exclude(pk=self.pk)

        if conflicting_appointments.exists():
            raise ValidationError(_("This time slot is already booked"))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        # إرسال إشعار للمريض
        if self.status == "confirmed" and not self.reminder_sent:
            from notifications.models import Notification

            Notification.objects.create(
                recipient=self.patient.user,
                title=_("Appointment Confirmed"),
                message=_(
                    f"Your appointment with Dr. {self.doctor.user.get_full_name()} on {self.appointment_date} has been confirmed."
                ),
                notification_type="appointment_confirmation",
            )
            self.reminder_sent = True
            super().save(update_fields=["reminder_sent"])


class WaitingList(models.Model):
    """نموذج قائمة الانتظار"""

    PRIORITY_WEIGHTS = {"normal": 1, "urgent": 2, "emergency": 3}

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="waiting_list_entries",
        verbose_name=_("Patient"),
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="waiting_lists",
        verbose_name=_("Doctor"),
    )

    reason = models.TextField(verbose_name=_("Reason for Visit"))

    priority = models.CharField(
        max_length=20,
        choices=Appointment.PRIORITY_CHOICES,
        default="normal",
        verbose_name=_("Priority"),
    )

    preferred_date = models.DateField(
        verbose_name=_("Preferred Date"),
        help_text=_("Preferred date for the appointment"),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    is_processed = models.BooleanField(default=False, verbose_name=_("Is Processed"))

    class Meta:
        verbose_name = _("Waiting List Entry")
        verbose_name_plural = _("Waiting List Entries")
        ordering = ["priority", "created_at"]

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.preferred_date}"

    def clean(self):
        """التحقق من صحة البيانات"""
        super().clean()

        if self.preferred_date < timezone.now().date():
            raise ValidationError(_("Preferred date cannot be in the past"))

    def calculate_priority_score(self) -> float:
        """
        حساب درجة الأولوية
        Calculate priority score based on various factors
        """
        # الوزن الأساسي حسب الأولوية
        base_score = self.PRIORITY_WEIGHTS.get(self.priority, 1)

        # حساب الوقت المنقضي منذ الإنشاء (بالأيام)
        waiting_time = ExpressionWrapper(
            Now() - F("created_at"),
            output_field=FloatField(),
        )
        days_waiting = waiting_time.days

        # معامل الوقت: 0.1 نقطة لكل يوم انتظار
        time_factor = days_waiting * 0.1

        return base_score + time_factor


class Schedule(models.Model):
    """نموذج جدول الدوام"""

    DAYS_OF_WEEK = [
        (0, _("Monday")),
        (1, _("Tuesday")),
        (2, _("Wednesday")),
        (3, _("Thursday")),
        (4, _("Friday")),
        (5, _("Saturday")),
        (6, _("Sunday")),
    ]

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="schedules",
        verbose_name=_("Doctor"),
    )

    day_of_week = models.IntegerField(
        choices=DAYS_OF_WEEK, verbose_name=_("Day of Week")
    )

    start_time = models.TimeField(verbose_name=_("Start Time"))
    end_time = models.TimeField(verbose_name=_("End Time"))

    break_start = models.TimeField(
        null=True, blank=True, verbose_name=_("Break Start Time")
    )
    break_end = models.TimeField(
        null=True, blank=True, verbose_name=_("Break End Time")
    )

    appointment_duration = models.IntegerField(
        default=30,
        help_text=_("Duration of each appointment in minutes"),
        verbose_name=_("Appointment Duration"),
    )

    is_available = models.BooleanField(default=True, verbose_name=_("Is Available"))

    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    class Meta:
        verbose_name = _("Schedule")
        verbose_name_plural = _("Schedules")
        ordering = ["day_of_week", "start_time"]
        unique_together = ["doctor", "day_of_week"]

    def __str__(self):
        return f"{self.doctor} - {self.get_day_of_week_display()}"

    def clean(self):
        """التحقق من صحة البيانات"""
        super().clean()

        if self.start_time >= self.end_time:
            raise ValidationError(_("End time must be after start time"))

        if self.break_start and self.break_end:
            if self.break_start >= self.break_end:
                raise ValidationError(_("Break end time must be after break start time"))

            if self.break_start < self.start_time:
                raise ValidationError(
                    _("Break start time must be after working hours start time")
                )

            if self.break_end > self.end_time:
                raise ValidationError(
                    _("Break end time must be before working hours end time")
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_available_slots(self, date):
        """
        الحصول على المواعيد المتاحة في تاريخ معين
        Get available appointment slots for a specific date

        Args:
            date (datetime.date): التاريخ المطلوب | The requested date

        Returns:
            list: قائمة بالمواعيد المتاحة | List of available time slots
        """
        if not self.is_available or date.weekday() != self.day_of_week:
            return []

        slots = []
        current_time = self.start_time
        while current_time <= self.end_time:
            # تخطي وقت الراحة
            if self.break_start and self.break_end:
                if self.break_start <= current_time <= self.break_end:
                    current_time = self.break_end
                    continue

            # التحقق من الحجوزات الموجودة
            slot_datetime = timezone.make_aware(
                timezone.datetime.combine(date, current_time)
            )
            is_booked = Appointment.objects.filter(
                doctor=self.doctor,
                appointment_date=slot_datetime,
                status__in=["pending", "confirmed"],
            ).exists()

            if not is_booked:
                slots.append(current_time)

            # الانتقال إلى الموعد التالي
            current_time = (
                timezone.datetime.combine(timezone.datetime.min, current_time)
                + timezone.timedelta(minutes=self.appointment_duration)
            ).time()

        return slots
