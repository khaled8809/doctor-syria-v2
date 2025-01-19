"""
وحدة نماذج الأطباء
Doctor Models Module

This module defines the data models for doctors, including:
- Basic doctor information
- Specializations
- Qualifications
"""

from typing import Any, Dict, List, Optional

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from patient_records.models import Patient


class Specialization(models.Model):
    """
    نموذج التخصص الطبي
    Medical Specialization Model

    Attributes:
        name: اسم التخصص | Specialization name
        description: وصف التخصص | Specialization description
    """

    name = models.CharField(_("اسم التخصص"), max_length=100, unique=True)
    description = models.TextField(_("وصف التخصص"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "doctor"
        verbose_name = _("تخصص")
        verbose_name_plural = _("التخصصات")
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def get_active_doctors(self) -> List["Doctor"]:
        """الحصول على الأطباء النشطين في هذا التخصص | Get active doctors in this specialization"""
        return self.doctors.filter(is_active=True)


class Doctor(models.Model):
    """
    نموذج بيانات الطبيب
    Doctor Model

    Attributes:
        user: المستخدم المرتبط | Associated user account
        specialization: التخصص | Medical specialization
        license_number: رقم الترخيص | Medical license number
        years_of_experience: سنوات الخبرة | Years of experience
        education: المؤهلات التعليمية | Educational qualifications
        bio: نبذة عن الطبيب | Doctor's biography
        is_available: متاح للمواعيد | Available for appointments
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctor_profile",
    )
    specialization = models.ForeignKey(
        Specialization, on_delete=models.PROTECT, related_name="doctors"
    )
    license_number = models.CharField(_("رقم الترخيص"), max_length=50, unique=True)
    years_of_experience = models.PositiveIntegerField(
        _("سنوات الخبرة"), validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    education = models.TextField(_("المؤهلات التعليمية"))
    bio = models.TextField(_("نبذة"), blank=True)
    is_available = models.BooleanField(_("متاح"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "doctor"
        verbose_name = _("طبيب")
        verbose_name_plural = _("الأطباء")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"د. {self.user.get_full_name()} ({self.specialization})"

    def get_upcoming_appointments(self) -> List["Appointment"]:
        """الحصول على المواعيد القادمة | Get upcoming appointments"""
        return self.appointments.filter(
            appointment_date__gte=timezone.now(), status="pending"
        ).order_by("appointment_date")

    def get_appointment_count(self) -> Dict[str, int]:
        """
        إحصائيات المواعيد
        Get appointment statistics

        Returns:
            Dict containing counts for different appointment statuses
        """
        return {
            "total": self.appointments.count(),
            "pending": self.appointments.filter(status="pending").count(),
            "confirmed": self.appointments.filter(status="confirmed").count(),
            "cancelled": self.appointments.filter(status="cancelled").count(),
            "completed": self.appointments.filter(status="completed").count(),
        }

    def get_rating(self) -> float:
        """
        متوسط تقييم الطبيب
        Get doctor's average rating

        Returns:
            float: Average rating between 0 and 5
        """
        ratings = self.reviews.filter(is_verified=True)
        if not ratings.exists():
            return 0.0
        return round(sum(r.rating for r in ratings) / ratings.count(), 1)


class Prescription(models.Model):
    """
    نموذج الوصفات الطبية
    Prescription Model

    Attributes:
        doctor: الطبيب | Associated doctor
        patient: المريض | Associated patient
        diagnosis: التشخيص | Diagnosis
        notes: الملاحظات | Notes
    """

    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="prescriptions"
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="prescriptions"
    )
    diagnosis = models.TextField(_("التشخيص"))
    notes = models.TextField(_("الملاحظات"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(_("فعال"), default=True)

    class Meta:
        app_label = "doctor"
        verbose_name = _("وصفة طبية")
        verbose_name_plural = _("الوصفات الطبية")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.doctor} - {self.patient} - {self.created_at}"


class PrescriptionItem(models.Model):
    """
    نموذج عنصر الوصفة الطبية
    Prescription Item Model

    Attributes:
        prescription: الوصفة الطبية | Associated prescription
        medicine_name: اسم الدواء | Medicine name
        dosage: الجرعة | Dosage
        frequency: التكرار | Frequency
        duration: المدة | Duration
        instructions: الإرشادات | Instructions
    """

    prescription = models.ForeignKey(
        Prescription, on_delete=models.CASCADE, related_name="items"
    )
    medicine_name = models.CharField(_("اسم الدواء"), max_length=100)
    dosage = models.CharField(_("الجرعة"), max_length=50)
    frequency = models.CharField(_("التكرار"), max_length=50)
    duration = models.CharField(_("المدة"), max_length=50)
    instructions = models.TextField(_("الإرشادات"))

    class Meta:
        app_label = "doctor"
        verbose_name = _("عنصر وصفة طبية")
        verbose_name_plural = _("عناصر الوصفات الطبية")
        ordering = ["prescription"]

    def __str__(self):
        return f"{self.medicine_name} - {self.prescription}"


class MedicalNote(models.Model):
    """
    نموذج الملاحظات الطبية
    Medical Note Model

    Attributes:
        doctor: الطبيب | Associated doctor
        patient: المريض | Associated patient
        note_type: نوع الملاحظة | Note type
        content: المحتوى | Content
    """

    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="medical_notes"
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="medical_notes"
    )
    note_type = models.CharField(_("نوع الملاحظة"), max_length=50)
    content = models.TextField(_("المحتوى"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "doctor"
        verbose_name = _("ملاحظة طبية")
        verbose_name_plural = _("الملاحظات الطبية")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.doctor} - {self.patient} - {self.note_type}"


class DoctorReview(models.Model):
    """
    نموذج تقييم الطبيب
    Doctor Review Model

    Attributes:
        doctor: الطبيب | Associated doctor
        patient: المريض | Associated patient
        rating: التقييم | Rating
        comment: التعليق | Comment
    """

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="reviews")
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.IntegerField(_("التقييم"))
    comment = models.TextField(_("التعليق"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(_("مؤكد"), default=False)

    class Meta:
        app_label = "doctor"
        verbose_name = _("تقييم طبيب")
        verbose_name_plural = _("تقييمات الأطباء")
        unique_together = ["doctor", "patient"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.doctor} - {self.patient} - {self.rating}"
