"""
Models for the appointments application.
"""
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.models import Doctor, Patient
from core.models import TimestampMixin


class Appointment(TimestampMixin):
    """
    Model for managing appointments.
    """
    STATUS_CHOICES = [
        ('pending', _('قيد الانتظار')),
        ('confirmed', _('مؤكد')),
        ('cancelled', _('ملغي')),
        ('completed', _('مكتمل')),
    ]

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name=_('الطبيب')
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name=_('المريض')
    )
    date = models.DateTimeField(
        verbose_name=_('تاريخ الموعد')
    )
    duration = models.IntegerField(
        default=30,
        verbose_name=_('مدة الموعد (بالدقائق)')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('حالة الموعد')
    )
    reason = models.TextField(
        blank=True,
        verbose_name=_('سبب الزيارة')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('ملاحظات')
    )

    class Meta:
        verbose_name = _('موعد')
        verbose_name_plural = _('المواعيد')
        ordering = ['-date']

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.date}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Only set for new appointments
            self.status = 'pending'
        super().save(*args, **kwargs)


class Prescription(models.Model):
    appointment = models.OneToOneField(
        Appointment, on_delete=models.CASCADE, related_name="prescription"
    )
    diagnosis = models.TextField()
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateField()

    def __str__(self):
        return f"Prescription for {self.appointment}"


class PrescriptionMedicine(models.Model):
    prescription = models.ForeignKey(
        Prescription, on_delete=models.CASCADE, related_name="medicines"
    )
    medicine_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.medicine_name} - {self.prescription}"


class MedicalRecord(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="medical_records"
    )
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="medical_records"
    )
    date = models.DateField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    notes = models.TextField(blank=True)
    attachments = models.FileField(upload_to="medical_records/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.date}"
