"""
Models for the accounts application.

This module defines all models related to user accounts, including:
- User profiles and authentication
- Doctor specializations
- Insurance information
"""
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from core.mixins import AuditMixin, SoftDeleteMixin, TimestampMixin

from .choices import (
    BloodType,
    GenderType,
    IdentificationType,
    MaritalStatus,
    SpecialtyType,
    UserType,
)
from .managers import CustomUserManager
from .validators import (
    validate_medical_license,
    validate_phone_number,
    validate_syrian_id,
)


class User(AbstractUser, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """
    نموذج المستخدم المخصص
    """

    username = None  # تعطيل حقل اسم المستخدم
    email = models.EmailField(
        _("البريد الإلكتروني"), unique=True, validators=[EmailValidator()]
    )
    phone = models.CharField(
        _("رقم الهاتف"),
        max_length=20,
        validators=[validate_phone_number],
        null=True,
        blank=True,
    )
    user_type = models.CharField(
        _("نوع المستخدم"),
        max_length=20,
        choices=UserType.choices,
        default=UserType.PATIENT,
    )

    # معلومات شخصية
    first_name = models.CharField(_("الاسم الأول"), max_length=150)
    last_name = models.CharField(_("الاسم الأخير"), max_length=150)
    father_name = models.CharField(_("اسم الأب"), max_length=150, blank=True)
    mother_name = models.CharField(_("اسم الأم"), max_length=150, blank=True)
    birth_date = models.DateField(_("تاريخ الميلاد"), null=True, blank=True)
    gender = models.CharField(
        _("الجنس"), max_length=1, choices=GenderType.choices, default=GenderType.MALE
    )
    marital_status = models.CharField(
        _("الحالة الاجتماعية"), max_length=10, choices=MaritalStatus.choices, blank=True
    )
    blood_type = models.CharField(
        _("فصيلة الدم"), max_length=3, choices=BloodType.choices, blank=True
    )

    # معلومات الهوية
    id_type = models.CharField(
        _("نوع الهوية"),
        max_length=20,
        choices=IdentificationType.choices,
        default=IdentificationType.NATIONAL_ID,
    )
    id_number = models.CharField(
        _("رقم الهوية"),
        max_length=20,
        validators=[validate_syrian_id],
        null=True,
        blank=True,
    )

    # معلومات الموقع
    address = models.TextField(_("العنوان"), blank=True)
    city = models.CharField(_("المدينة"), max_length=100, blank=True)
    region = models.CharField(_("المنطقة"), max_length=100, blank=True)

    # معلومات إضافية للأطباء
    specialty = models.CharField(
        _("التخصص"), max_length=50, choices=SpecialtyType.choices, blank=True
    )
    license_number = models.CharField(
        _("رقم الترخيص"),
        max_length=20,
        validators=[validate_medical_license],
        blank=True,
    )
    qualification = models.CharField(_("المؤهل العلمي"), max_length=200, blank=True)
    experience_years = models.PositiveIntegerField(_("سنوات الخبرة"), default=0)

    # معلومات إضافية للشركات
    company_name = models.CharField(_("اسم الشركة"), max_length=200, blank=True)
    registration_number = models.CharField(
        _("رقم السجل التجاري"), max_length=50, blank=True
    )

    # الصور
    profile_picture = models.ImageField(
        _("الصورة الشخصية"), upload_to="profile_pictures/", null=True, blank=True
    )
    id_picture = models.ImageField(
        _("صورة الهوية"), upload_to="id_pictures/", null=True, blank=True
    )
    license_picture = models.ImageField(
        _("صورة الترخيص"), upload_to="license_pictures/", null=True, blank=True
    )

    # إعدادات الحساب
    is_verified = models.BooleanField(_("تم التحقق"), default=False)
    verification_date = models.DateTimeField(_("تاريخ التحقق"), null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(
        _("آخر عنوان IP"), null=True, blank=True
    )

    # حقول التتبع
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), default=timezone.now)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)
    deleted_at = models.DateTimeField(_("تاريخ الحذف"), null=True, blank=True)
    is_deleted = models.BooleanField(_("محذوف"), default=False)

    # حقول التدقيق
    created_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_users",
        verbose_name=_("تم الإنشاء بواسطة"),
    )
    updated_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_users",
        verbose_name=_("تم التحديث بواسطة"),
    )
    deleted_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deleted_users",
        verbose_name=_("تم الحذف بواسطة"),
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone", "first_name", "last_name", "user_type"]

    class Meta:
        verbose_name = _("مستخدم")
        verbose_name_plural = _("المستخدمين")
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    def get_full_name(self):
        """
        إرجاع الاسم الكامل للمستخدم
        """
        full_name = f"{self.first_name} {self.father_name} {self.last_name}"
        return full_name.strip()

    def soft_delete(self, deleted_by=None):
        """
        حذف ناعم للمستخدم
        """
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = deleted_by
        self.save()

    def restore(self):
        """
        استعادة المستخدم المحذوف
        """
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.save()

    @property
    def is_doctor(self):
        return self.user_type == UserType.DOCTOR

    @property
    def is_patient(self):
        return self.user_type == UserType.PATIENT

    @property
    def is_pharmacy(self):
        return self.user_type == UserType.PHARMACY

    @property
    def is_lab(self):
        return self.user_type == UserType.LAB

    @property
    def is_hospital(self):
        return self.user_type == UserType.HOSPITAL

    @property
    def is_company(self):
        return self.user_type == UserType.COMPANY


class Area(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.city}"


class Clinic(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="clinics/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def average_rating(self):
        return self.review_set.aggregate(Avg("rating"))["rating__avg"] or 0

    def __str__(self):
        return self.name


class Hospital(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="hospitals/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def average_rating(self):
        return self.review_set.aggregate(Avg("rating"))["rating__avg"] or 0

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="doctor_profile"
    )
    specialization = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, blank=True)
    hospital = models.ForeignKey(
        Hospital, on_delete=models.SET_NULL, null=True, blank=True
    )
    experience_years = models.IntegerField(default=0)
    education = models.TextField(blank=True, default="")
    certifications = models.TextField(blank=True)
    license_number = models.CharField(max_length=50, unique=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    available_for_online = models.BooleanField(default=False)

    @property
    def average_rating(self):
        return self.review_set.aggregate(Avg("rating"))["rating__avg"] or 0

    def __str__(self):
        return f"د. {self.user.get_full_name()}"


class Patient(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="patient_profile"
    )
    date_of_birth = models.DateField(null=True, blank=True)
    blood_type = models.CharField(max_length=5, blank=True)
    allergies = models.TextField(blank=True)
    chronic_diseases = models.TextField(blank=True)

    def __str__(self):
        return self.user.get_full_name()


class Pharmacy(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="pharmacy_profile"
    )
    license_number = models.CharField(max_length=50, unique=True)
    opening_hours = models.CharField(max_length=100)
    delivery_available = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()


class Laboratory(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="laboratory_profile"
    )
    license_number = models.CharField(max_length=50, unique=True)
    services = models.TextField()
    opening_hours = models.CharField(max_length=100)

    def __str__(self):
        return self.user.get_full_name()


class PharmaceuticalCompany(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="company_profile"
    )
    license_number = models.CharField(max_length=50, unique=True)
    registration_number = models.CharField(max_length=50, unique=True)
    company_size = models.CharField(max_length=50)

    def __str__(self):
        return self.user.get_full_name()


class Nurse(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="nurse_profile"
    )
    department = models.ForeignKey(
        "hms.Department", on_delete=models.SET_NULL, null=True
    )
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    years_of_experience = models.IntegerField()

    def __str__(self):
        return f"{self.user.get_full_name()} - Nurse"


class Staff(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="staff_profile"
    )
    department = models.ForeignKey(
        "hms.Department", on_delete=models.SET_NULL, null=True
    )
    position = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50, unique=True)
    hire_date = models.DateField()

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"


class Specialization(models.Model):
    """
    Medical specializations for doctors
    """
    name = models.CharField(_('الاسم'), max_length=100)
    description = models.TextField(_('الوصف'), blank=True)
    
    class Meta:
        verbose_name = _('تخصص')
        verbose_name_plural = _('التخصصات')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class DoctorProfile(models.Model):
    """
    Doctor profile model
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='doctor_profile',
        verbose_name=_('المستخدم')
    )
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.SET_NULL,
        null=True,
        related_name='doctors',
        verbose_name=_('التخصص')
    )
    license_number = models.CharField(_('رقم الترخيص'), max_length=50)
    years_of_experience = models.PositiveIntegerField(
        _('سنوات الخبرة'),
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    bio = models.TextField(_('السيرة الذاتية'), blank=True)
    consultation_fee = models.DecimalField(
        _('رسوم الاستشارة'),
        max_digits=10,
        decimal_places=2,
        default=0
    )
    available_for_online = models.BooleanField(
        _('متاح للاستشارات عبر الإنترنت'),
        default=True
    )
    rating = models.FloatField(
        _('التقييم'),
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0
    )
    
    class Meta:
        verbose_name = _('طبيب')
        verbose_name_plural = _('الأطباء')
        ordering = ['-rating', 'user__first_name']
    
    def __str__(self):
        return f"د. {self.user.get_full_name()}"


class PatientProfile(models.Model):
    """
    Patient profile model
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='patient_profile',
        verbose_name=_('المستخدم')
    )
    blood_type = models.CharField(
        _('فصيلة الدم'),
        max_length=5,
        choices=(
            ('A+', 'A+'), ('A-', 'A-'),
            ('B+', 'B+'), ('B-', 'B-'),
            ('O+', 'O+'), ('O-', 'O-'),
            ('AB+', 'AB+'), ('AB-', 'AB-')
        ),
        blank=True
    )
    emergency_contact_name = models.CharField(
        _('اسم جهة الاتصال في الطوارئ'),
        max_length=100,
        blank=True
    )
    emergency_contact_phone = models.CharField(
        _('رقم هاتف الطوارئ'),
        max_length=20,
        blank=True
    )
    height = models.FloatField(
        _('الطول (سم)'),
        validators=[MinValueValidator(0), MaxValueValidator(300)],
        null=True,
        blank=True
    )
    weight = models.FloatField(
        _('الوزن (كجم)'),
        validators=[MinValueValidator(0), MaxValueValidator(500)],
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = _('مريض')
        verbose_name_plural = _('المرضى')
        ordering = ['user__first_name']
    
    def __str__(self):
        return self.user.get_full_name()


class Insurance(models.Model):
    """
    Insurance information model
    """
    patient = models.ForeignKey(
        PatientProfile,
        on_delete=models.CASCADE,
        related_name='insurance_info',
        verbose_name=_('المريض')
    )
    provider = models.CharField(_('مزود التأمين'), max_length=100)
    policy_number = models.CharField(_('رقم البوليصة'), max_length=50)
    start_date = models.DateField(_('تاريخ البداية'))
    end_date = models.DateField(_('تاريخ النهاية'))
    coverage_type = models.CharField(_('نوع التغطية'), max_length=50)
    coverage_percentage = models.FloatField(
        _('نسبة التغطية'),
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    max_coverage_amount = models.DecimalField(
        _('الحد الأقصى للتغطية'),
        max_digits=10,
        decimal_places=2
    )
    notes = models.TextField(_('ملاحظات'), blank=True)
    
    class Meta:
        verbose_name = _('تأمين')
        verbose_name_plural = _('التأمينات')
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.patient} - {self.provider}"


class DoctorAvailability(models.Model):
    """
    Doctor availability schedule
    """
    DAYS_OF_WEEK = (
        (0, _('الاثنين')),
        (1, _('الثلاثاء')),
        (2, _('الأربعاء')),
        (3, _('الخميس')),
        (4, _('الجمعة')),
        (5, _('السبت')),
        (6, _('الأحد')),
    )
    
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name='availability',
        verbose_name=_('الطبيب')
    )
    day_of_week = models.IntegerField(_('اليوم'), choices=DAYS_OF_WEEK)
    start_time = models.TimeField(_('وقت البداية'))
    end_time = models.TimeField(_('وقت النهاية'))
    is_available = models.BooleanField(_('متاح'), default=True)
    break_start = models.TimeField(_('بداية الاستراحة'), null=True, blank=True)
    break_end = models.TimeField(_('نهاية الاستراحة'), null=True, blank=True)
    max_appointments = models.PositiveIntegerField(
        _('الحد الأقصى للمواعيد'),
        default=20
    )
    appointment_duration = models.DurationField(
        _('مدة الموعد'),
        default=timezone.timedelta(minutes=30)
    )
    notes = models.TextField(_('ملاحظات'), blank=True)
    
    class Meta:
        verbose_name = _('جدول الطبيب')
        verbose_name_plural = _('جداول الأطباء')
        ordering = ['day_of_week', 'start_time']
        unique_together = ['doctor', 'day_of_week']
    
    def __str__(self):
        return f"{self.doctor} - {self.get_day_of_week_display()}"
