from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Avg
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from core.mixins import TimestampMixin, SoftDeleteMixin, AuditMixin
from .managers import CustomUserManager
from .validators import (
    validate_phone_number,
    validate_syrian_id,
    validate_medical_license,
)
from .choices import (
    UserType,
    GenderType,
    MaritalStatus,
    BloodType,
    SpecialtyType,
    IdentificationType,
)
from django.utils import timezone


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
