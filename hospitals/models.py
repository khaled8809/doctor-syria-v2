"""
نماذج بيانات المستشفيات
"""

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User


class Hospital(models.Model):
    """نموذج المستشفى"""

    name = models.CharField(_("اسم المستشفى"), max_length=255)
    license_number = models.CharField(_("رقم الترخيص"), max_length=50, unique=True)
    description = models.TextField(_("وصف المستشفى"), blank=True)
    address = models.TextField(_("العنوان"))
    phone = models.CharField(_("رقم الهاتف"), max_length=20)
    email = models.EmailField(_("البريد الإلكتروني"))
    website = models.URLField(_("الموقع الإلكتروني"), blank=True)
    logo = models.ImageField(
        _("شعار المستشفى"), upload_to="hospitals/logos/", blank=True
    )

    # معلومات إضافية
    established_date = models.DateField(_("تاريخ التأسيس"))
    is_active = models.BooleanField(_("نشط"), default=True)
    is_24_hours = models.BooleanField(_("خدمة 24 ساعة"), default=False)
    has_emergency = models.BooleanField(_("قسم طوارئ"), default=False)
    has_ambulance = models.BooleanField(_("خدمة إسعاف"), default=False)

    # إحصائيات
    bed_capacity = models.PositiveIntegerField(
        _("عدد الأسرّة"), validators=[MinValueValidator(1)]
    )
    icu_capacity = models.PositiveIntegerField(
        _("عدد أسرّة العناية المركزة"), validators=[MinValueValidator(0)]
    )
    operating_rooms = models.PositiveIntegerField(
        _("عدد غرف العمليات"), validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = _("مستشفى")
        verbose_name_plural = _("المستشفيات")

    def __str__(self):
        return self.name


class Department(models.Model):
    """نموذج قسم المستشفى"""

    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name="departments"
    )
    name = models.CharField(_("اسم القسم"), max_length=100)
    description = models.TextField(_("وصف القسم"), blank=True)
    floor = models.CharField(_("الطابق"), max_length=50)
    is_active = models.BooleanField(_("نشط"), default=True)
    head_doctor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role": "doctor"},
        related_name="headed_departments",
    )

    class Meta:
        verbose_name = _("قسم")
        verbose_name_plural = _("الأقسام")
        unique_together = ["hospital", "name"]

    def __str__(self):
        return f"{self.name} - {self.hospital.name}"


class Room(models.Model):
    """نموذج غرفة المستشفى"""

    ROOM_TYPES = [
        ("normal", _("غرفة عادية")),
        ("icu", _("عناية مركزة")),
        ("operation", _("غرفة عمليات")),
        ("emergency", _("غرفة طوارئ")),
        ("examination", _("غرفة فحص")),
    ]

    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="rooms"
    )
    room_number = models.CharField(_("رقم الغرفة"), max_length=50)
    room_type = models.CharField(_("نوع الغرفة"), max_length=20, choices=ROOM_TYPES)
    capacity = models.PositiveIntegerField(
        _("السعة"), validators=[MinValueValidator(1)]
    )
    is_available = models.BooleanField(_("متاحة"), default=True)
    notes = models.TextField(_("ملاحظات"), blank=True)

    class Meta:
        verbose_name = _("غرفة")
        verbose_name_plural = _("الغرف")
        unique_together = ["department", "room_number"]

    def __str__(self):
        return (
            f"{self.room_number} - {self.get_room_type_display()} - {self.department}"
        )


class Equipment(models.Model):
    """نموذج المعدات الطبية"""

    EQUIPMENT_STATUS = [
        ("active", _("نشط")),
        ("maintenance", _("صيانة")),
        ("broken", _("معطل")),
        ("retired", _("متقاعد")),
    ]

    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name="equipment"
    )
    name = models.CharField(_("اسم المعدات"), max_length=255)
    serial_number = models.CharField(_("الرقم التسلسلي"), max_length=100, unique=True)
    manufacturer = models.CharField(_("الشركة المصنعة"), max_length=255)
    model = models.CharField(_("الموديل"), max_length=100)
    purchase_date = models.DateField(_("تاريخ الشراء"))
    warranty_expiry = models.DateField(_("تاريخ انتهاء الضمان"))
    status = models.CharField(
        _("الحالة"), max_length=20, choices=EQUIPMENT_STATUS, default="active"
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="equipment",
    )
    room = models.ForeignKey(
        Room, on_delete=models.SET_NULL, null=True, blank=True, related_name="equipment"
    )
    notes = models.TextField(_("ملاحظات"), blank=True)

    class Meta:
        verbose_name = _("معدات")
        verbose_name_plural = _("المعدات")

    def __str__(self):
        return f"{self.name} - {self.serial_number}"


class Staff(models.Model):
    """نموذج الكادر الطبي"""

    STAFF_TYPES = [
        ("doctor", _("طبيب")),
        ("nurse", _("ممرض/ة")),
        ("technician", _("فني")),
        ("admin", _("إداري")),
        ("other", _("آخر")),
    ]

    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name="staff"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="hospital_positions"
    )
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="staff"
    )
    staff_type = models.CharField(_("نوع الوظيفة"), max_length=20, choices=STAFF_TYPES)
    start_date = models.DateField(_("تاريخ البدء"))
    end_date = models.DateField(_("تاريخ الانتهاء"), null=True, blank=True)
    is_active = models.BooleanField(_("نشط"), default=True)
    notes = models.TextField(_("ملاحظات"), blank=True)

    class Meta:
        verbose_name = _("موظف")
        verbose_name_plural = _("الموظفين")
        unique_together = ["hospital", "user", "department"]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_staff_type_display()} - {self.department}"


class Shift(models.Model):
    """نموذج المناوبات"""

    SHIFT_TYPES = [
        ("morning", _("صباحي")),
        ("evening", _("مسائي")),
        ("night", _("ليلي")),
        ("on_call", _("تحت الطلب")),
    ]

    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name="shifts"
    )
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="shifts"
    )
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="shifts")
    shift_type = models.CharField(_("نوع المناوبة"), max_length=20, choices=SHIFT_TYPES)
    start_time = models.DateTimeField(_("وقت البدء"))
    end_time = models.DateTimeField(_("وقت الانتهاء"))
    notes = models.TextField(_("ملاحظات"), blank=True)

    class Meta:
        verbose_name = _("مناوبة")
        verbose_name_plural = _("المناوبات")

    def __str__(self):
        return f"{self.staff.user.get_full_name()} - {self.get_shift_type_display()} - {self.start_time.date()}"
