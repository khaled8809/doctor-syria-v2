"""
نماذج تطبيق الحسابات
يحتوي على نموذج المستخدم المخصص والنماذج المرتبطة به
"""

import os
import re
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from core.image_config import IMAGE_SETTINGS, LAZY_LOADING_SETTINGS
from core.utils import get_cached_image_url, optimize_image


def validate_phone_number(value):
    """التحقق من صحة رقم الهاتف"""
    if not re.match(r"^\+?1?\d{9,15}$", str(value)):
        raise ValidationError(
            _("%(value)s ليس رقم هاتف صحيح"),
            params={"value": value},
        )


def validate_license_number(value):
    """التحقق من صحة رقم الترخيص"""
    if not re.match(r"^[A-Z0-9]{5,15}$", str(value)):
        raise ValidationError(
            _("%(value)s ليس رقم ترخيص صحيح"),
            params={"value": value},
        )


class MedicalInformation(models.Model):
    """نموذج المعلومات الطبية للمستخدم"""

    user = models.OneToOneField(
        "User",
        on_delete=models.CASCADE,
        related_name="medical_info",
        verbose_name=_("المستخدم"),
    )

    blood_type = models.CharField(
        max_length=5,
        blank=True,
        verbose_name=_("فصيلة الدم"),
        choices=[
            ("A+", "A+"),
            ("A-", "A-"),
            ("B+", "B+"),
            ("B-", "B-"),
            ("AB+", "AB+"),
            ("AB-", "AB-"),
            ("O+", "O+"),
            ("O-", "O-"),
        ],
    )

    allergies = models.TextField(blank=True, verbose_name=_("الحساسية"))

    chronic_diseases = models.TextField(blank=True, verbose_name=_("الأمراض المزمنة"))

    emergency_contact = models.CharField(
        max_length=100, blank=True, verbose_name=_("جهة اتصال للطوارئ")
    )

    emergency_phone = PhoneNumberField(
        null=True,
        blank=True,
        verbose_name=_("هاتف الطوارئ"),
        validators=[validate_phone_number],
    )

    class Meta:
        verbose_name = _("معلومات طبية")
        verbose_name_plural = _("معلومات طبية")

    def __str__(self):
        return f"المعلومات الطبية لـ {self.user.get_full_name()}"


def user_directory_path(instance, filename):
    return f"users/{instance.id}/{filename}"


class User(AbstractUser):
    """نموذج المستخدم المخصص
    يوفر وظائف إضافية للمستخدمين مثل الأدوار والمصادقة الثنائية
    """

    class Roles(models.TextChoices):
        ADMIN = "admin", _("مدير")
        DOCTOR = "doctor", _("طبيب")
        NURSE = "nurse", _("ممرض")
        PHARMACIST = "pharmacist", _("صيدلي")
        LAB_TECHNICIAN = "lab_technician", _("فني مختبر")
        RECEPTIONIST = "receptionist", _("موظف استقبال")
        PATIENT = "patient", _("مريض")

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.PATIENT,
        verbose_name=_("الدور"),
    )

    phone = PhoneNumberField(
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("رقم الهاتف"),
        validators=[validate_phone_number],
    )

    address = models.TextField(blank=True, verbose_name=_("العنوان"))

    birth_date = models.DateField(
        null=True, blank=True, verbose_name=_("تاريخ الميلاد")
    )

    profile_picture = models.ImageField(
        upload_to=user_directory_path,
        null=True,
        blank=True,
        verbose_name=_("الصورة الشخصية"),
    )

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if self.profile_picture and (
            is_new or "profile_picture" in self.get_dirty_fields()
        ):
            optimize_image(self.profile_picture.path)

    def get_profile_picture_url(self, size="medium"):
        if not self.profile_picture:
            return None
        return get_cached_image_url(self.profile_picture, size)

    specialization = models.CharField(
        max_length=100, blank=True, verbose_name=_("التخصص")
    )

    license_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("رقم الترخيص"),
        validators=[validate_license_number],
    )

    two_factor_enabled = models.BooleanField(
        default=False, verbose_name=_("تفعيل المصادقة الثنائية")
    )

    two_factor_secret = models.CharField(
        max_length=32, null=True, blank=True, verbose_name=_("سر المصادقة الثنائية")
    )

    email_verified = models.BooleanField(
        default=False, verbose_name=_("تم التحقق من البريد")
    )

    failed_login_attempts = models.PositiveIntegerField(
        default=0, verbose_name=_("محاولات تسجيل الدخول الفاشلة")
    )

    account_locked_until = models.DateTimeField(
        null=True, blank=True, verbose_name=_("الحساب مقفل حتى")
    )

    last_password_change = models.DateTimeField(
        default=timezone.now, verbose_name=_("آخر تغيير لكلمة المرور")
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("تاريخ الإنشاء")
    )

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("تاريخ التحديث"))

    last_login_ip = models.GenericIPAddressField(
        null=True, blank=True, verbose_name=_("آخر عنوان IP")
    )

    last_activity = models.DateTimeField(
        null=True, blank=True, verbose_name=_("آخر نشاط")
    )

    device_info = models.JSONField(default=dict, verbose_name=_("معلومات الأجهزة"))

    barcode = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("الباركود")
    )

    id_card = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("البطاقة التعريفية")
    )

    class Meta:
        verbose_name = _("مستخدم")
        verbose_name_plural = _("المستخدمين")

    def __str__(self):
        """تمثيل نصي للمستخدم"""
        return f"{self.get_full_name()} ({self.username})"

    def clean(self):
        """التحقق من صحة البيانات"""
        super().clean()
        if self.is_doctor() and not self.license_number:
            raise ValidationError({"license_number": _("رقم الترخيص مطلوب للأطباء")})

    def get_role(self):
        """الحصول على الدور بالصيغة المعروضة"""
        return self.get_role_display()

    def is_doctor(self):
        """التحقق مما إذا كان المستخدم طبيباً"""
        return self.role == self.Roles.DOCTOR

    def is_nurse(self):
        """التحقق مما إذا كان المستخدم ممرضاً"""
        return self.role == self.Roles.NURSE

    def is_pharmacist(self):
        """التحقق مما إذا كان المستخدم صيدلياً"""
        return self.role == self.Roles.PHARMACIST

    def is_lab_technician(self):
        """التحقق مما إذا كان المستخدم فني مختبر"""
        return self.role == self.Roles.LAB_TECHNICIAN

    def is_receptionist(self):
        """التحقق مما إذا كان المستخدم موظف استقبال"""
        return self.role == self.Roles.RECEPTIONIST

    def is_patient(self):
        """التحقق مما إذا كان المستخدم مريضاً"""
        return self.role == self.Roles.PATIENT

    def is_medical_staff(self):
        """التحقق مما إذا كان المستخدم من الطاقم الطبي"""
        return self.is_doctor() or self.is_nurse()

    def is_support_staff(self):
        """التحقق مما إذا كان المستخدم من الطاقم المساند"""
        return (
            self.is_pharmacist() or self.is_lab_technician() or self.is_receptionist()
        )

    def is_locked(self):
        """التحقق مما إذا كان الحساب مقفلاً"""
        if not self.account_locked_until:
            return False
        return timezone.now() < self.account_locked_until

    def increment_failed_login(self):
        """زيادة عدد محاولات تسجيل الدخول الفاشلة"""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:  # قفل الحساب بعد 5 محاولات فاشلة
            self.account_locked_until = timezone.now() + timedelta(minutes=30)
        self.save()

    def reset_failed_login(self):
        """إعادة تعيين محاولات تسجيل الدخول الفاشلة"""
        self.failed_login_attempts = 0
        self.account_locked_until = None
        self.save()

    def update_last_activity(self):
        """تحديث آخر نشاط للمستخدم"""
        self.last_activity = timezone.now()
        self.save()

    def add_device_info(self, device_info):
        """إضافة معلومات جهاز جديد"""
        if not isinstance(self.device_info, dict):
            self.device_info = {}
        device_id = device_info.get("device_id")
        if device_id:
            self.device_info[device_id] = device_info
            self.save()

    def get_recent_activities(self):
        """الحصول على النشاطات الأخيرة للمستخدم"""
        # يمكن تنفيذ هذه الوظيفة لاحقاً
        pass
