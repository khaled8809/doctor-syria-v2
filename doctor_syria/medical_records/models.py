from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.models import Doctor, Patient
from core.models import AuditMixin, SoftDeleteMixin, TimestampMixin

from .choices import (
    AllergyReaction,
    AllergyType,
    AppointmentStatus,
    AppointmentType,
    RecordType,
    Severity,
    VaccinationType,
)


class MedicalRecord(TimestampMixin, SoftDeleteMixin, AuditMixin):
    """الملف الطبي الأساسي"""

    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    blood_type = models.CharField(
        max_length=5,
        choices=[
            ("A+", "A+"),
            ("A-", "A-"),
            ("B+", "B+"),
            ("B-", "B-"),
            ("O+", "O+"),
            ("O-", "O-"),
            ("AB+", "AB+"),
            ("AB-", "AB-"),
        ],
    )
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text="بالسنتيمتر")
    weight = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="بالكيلوغرام"
    )
    allergies = models.TextField(blank=True)
    chronic_conditions = models.TextField(blank=True)
    family_history = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100)
    emergency_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.PROTECT,
        related_name="doctor_records",
        verbose_name=_("الطبيب"),
    )
    record_type = models.CharField(
        _("نوع السجل"), max_length=20, choices=RecordType.choices
    )
    title = models.CharField(_("العنوان"), max_length=200)
    description = models.TextField(_("الوصف"))
    date = models.DateTimeField(_("التاريخ"), default=timezone.now)
    severity = models.CharField(
        _("مستوى الخطورة"),
        max_length=10,
        choices=Severity.choices,
        default=Severity.LOW,
    )
    notes = models.TextField(_("ملاحظات"), blank=True)
    attachments = models.FileField(
        _("المرفقات"), upload_to="medical_records/", null=True, blank=True
    )

    class Meta:
        verbose_name = _("سجل طبي")
        verbose_name_plural = _("السجلات الطبية")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.get_record_type_display()} - {self.date}"

    @property
    def bmi(self):
        """حساب مؤشر كتلة الجسم"""
        height_m = float(self.height) / 100
        return round(float(self.weight) / (height_m * height_m), 2)


class VitalSigns(models.Model):
    """المؤشرات الحيوية"""

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField()
    blood_pressure_systolic = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(300)]
    )
    blood_pressure_diastolic = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(200)]
    )
    heart_rate = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(250)]
    )
    temperature = models.DecimalField(max_digits=4, decimal_places=1)
    blood_sugar = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)]
    )
    oxygen_saturation = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"مؤشرات {self.patient.user.get_full_name()} في {self.date}"


class Medication(models.Model):
    """الأدوية والجرعات"""

    FREQUENCY_CHOICES = [
        ("daily", "يومياً"),
        ("twice_daily", "مرتين يومياً"),
        ("three_times", "ثلاث مرات يومياً"),
        ("four_times", "أربع مرات يومياً"),
        ("weekly", "أسبوعياً"),
        ("monthly", "شهرياً"),
        ("as_needed", "عند الحاجة"),
    ]

    STATUS_CHOICES = [
        ("active", "نشط"),
        ("completed", "مكتمل"),
        ("discontinued", "متوقف"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    prescribing_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.patient.user.get_full_name()}"

    @property
    def is_active(self):
        return self.status == "active" and (
            not self.end_date or self.end_date >= timezone.now().date()
        )


class MedicationReminder(models.Model):
    """تذكير بمواعيد الأدوية"""

    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    time = models.TimeField()
    is_taken = models.BooleanField(default=False)
    taken_at = models.DateTimeField(null=True, blank=True)
    skipped = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def mark_as_taken(self):
        self.is_taken = True
        self.taken_at = timezone.now()
        self.save()


class Appointment(TimestampMixin, SoftDeleteMixin, AuditMixin):
    """المواعيد الطبية"""

    STATUS_CHOICES = [
        ("scheduled", "مجدول"),
        ("confirmed", "مؤكد"),
        ("completed", "مكتمل"),
        ("cancelled", "ملغي"),
        ("no_show", "لم يحضر"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_type = models.CharField(
        _("نوع الموعد"), max_length=20, choices=AppointmentType.choices
    )
    status = models.CharField(
        _("حالة الموعد"),
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.PENDING,
    )
    scheduled_time = models.DateTimeField(_("وقت الموعد"))
    duration = models.PositiveIntegerField(
        _("المدة (بالدقائق)"),
        default=30,
        validators=[MinValueValidator(15), MaxValueValidator(180)],
    )
    reason = models.TextField(_("سبب الزيارة"))
    notes = models.TextField(_("ملاحظات"), blank=True)
    cancellation_reason = models.TextField(_("سبب الإلغاء"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("موعد")
        verbose_name_plural = _("المواعيد")
        ordering = ["-scheduled_time"]
        indexes = [
            models.Index(fields=["doctor", "scheduled_time"]),
            models.Index(fields=["patient", "scheduled_time"]),
            models.Index(fields=["status", "scheduled_time"]),
        ]

    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.doctor.user.get_full_name()} - {self.scheduled_time}"

    def cancel(self, reason):
        """
        إلغاء الموعد
        """
        self.status = AppointmentStatus.CANCELLED
        self.cancellation_reason = reason
        self.save()


class HealthGoal(models.Model):
    """أهداف صحية"""

    TYPE_CHOICES = [
        ("weight", "الوزن"),
        ("exercise", "التمارين"),
        ("diet", "النظام الغذائي"),
        ("blood_pressure", "ضغط الدم"),
        ("blood_sugar", "سكر الدم"),
        ("other", "أخرى"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_value = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    start_date = models.DateField()
    target_date = models.DateField()
    achieved = models.BooleanField(default=False)
    achieved_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.patient.user.get_full_name()}"


class ProgressUpdate(models.Model):
    """تحديثات التقدم"""

    goal = models.ForeignKey(HealthGoal, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.DecimalField(max_digits=8, decimal_places=2)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"تحديث {self.goal.title} - {self.date}"


class LabResult(models.Model):
    """نتائج التحاليل المخبرية"""

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=200)
    test_date = models.DateField()
    result_value = models.CharField(max_length=100)
    normal_range = models.CharField(max_length=100)
    is_normal = models.BooleanField()
    lab_name = models.CharField(max_length=200)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to="lab_results/", null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-test_date"]

    def __str__(self):
        return f"{self.test_name} - {self.patient.user.get_full_name()}"


class Vaccination(models.Model):
    """سجل التطعيمات"""

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    vaccine_name = models.CharField(max_length=200)
    dose_number = models.PositiveIntegerField()
    date_given = models.DateField()
    next_due_date = models.DateField(null=True, blank=True)
    administered_by = models.CharField(max_length=200)
    batch_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date_given"]

    def __str__(self):
        return f"{self.vaccine_name} - {self.patient.user.get_full_name()}"


class Prescription(TimestampMixin, SoftDeleteMixin, AuditMixin):
    """
    الوصفات الطبية
    """

    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.PROTECT,
        related_name="prescriptions",
        verbose_name=_("السجل الطبي"),
    )
    medicine_name = models.CharField(_("اسم الدواء"), max_length=200)
    dosage = models.CharField(_("الجرعة"), max_length=100)
    frequency = models.CharField(_("عدد مرات الأخذ"), max_length=100)
    duration = models.CharField(_("مدة العلاج"), max_length=100)
    instructions = models.TextField(_("تعليمات"), blank=True)
    is_chronic = models.BooleanField(_("دواء مزمن"), default=False)
    refills = models.PositiveIntegerField(_("عدد مرات إعادة الصرف"), default=0)
    notes = models.TextField(_("ملاحظات"), blank=True)

    class Meta:
        verbose_name = _("وصفة طبية")
        verbose_name_plural = _("الوصفات الطبية")
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.medicine_name} - {self.medical_record.patient.user.get_full_name()}"
        )


class Allergy(TimestampMixin, SoftDeleteMixin, AuditMixin):
    """
    الحساسية
    """

    patient = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="patient_allergies",
        limit_choices_to={"user_type": "patient"},
        verbose_name=_("المريض"),
    )
    allergy_type = models.CharField(
        _("نوع الحساسية"), max_length=20, choices=AllergyType.choices
    )
    allergen = models.CharField(_("المسبب"), max_length=200)
    reaction = models.CharField(
        _("رد الفعل"), max_length=20, choices=AllergyReaction.choices
    )
    diagnosis_date = models.DateField(_("تاريخ التشخيص"))
    notes = models.TextField(_("ملاحظات"), blank=True)

    class Meta:
        verbose_name = _("حساسية")
        verbose_name_plural = _("الحساسيات")
        ordering = ["-diagnosis_date"]
        unique_together = ["patient", "allergen"]

    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.allergen}"


class AllergyReaction(models.Model):
    """
    ردود أفعال الحساسية
    """

    allergy = models.ForeignKey(
        Allergy,
        on_delete=models.CASCADE,
        related_name="reactions",
        verbose_name=_("الحساسية"),
    )
    reaction = models.CharField(_("رد الفعل"), max_length=200)
    notes = models.TextField(_("ملاحظات"), blank=True)

    def __str__(self):
        return f"{self.allergy.patient.user.get_full_name()} - {self.reaction}"


class Vaccination(TimestampMixin, SoftDeleteMixin, AuditMixin):
    """
    التطعيمات
    """

    patient = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="patient_vaccinations",
        limit_choices_to={"user_type": "patient"},
        verbose_name=_("المريض"),
    )
    vaccine_type = models.CharField(
        _("نوع التطعيم"), max_length=20, choices=VaccinationType.choices
    )
    vaccine_name = models.CharField(_("اسم التطعيم"), max_length=200)
    dose_number = models.PositiveIntegerField(_("رقم الجرعة"), default=1)
    date_given = models.DateField(_("تاريخ الأخذ"))
    given_by = models.ForeignKey(
        Doctor,
        on_delete=models.PROTECT,
        related_name="administered_vaccinations",
        verbose_name=_("الطبيب المعطي"),
    )
    next_dose_date = models.DateField(_("تاريخ الجرعة القادمة"), null=True, blank=True)
    batch_number = models.CharField(_("رقم التشغيلة"), max_length=50, blank=True)
    manufacturer = models.CharField(_("الشركة المصنعة"), max_length=200, blank=True)
    notes = models.TextField(_("ملاحظات"), blank=True)

    class Meta:
        verbose_name = _("تطعيم")
        verbose_name_plural = _("التطعيمات")
        ordering = ["-date_given"]
        unique_together = ["patient", "vaccine_type", "dose_number"]

    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.vaccine_name} - الجرعة {self.dose_number}"


class MedicalHistory(TimestampMixin):
    """
    Patient medical history model
    """
    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name='medical_history',
        verbose_name=_('المريض')
    )
    family_history = models.TextField(_('التاريخ العائلي'), blank=True)
    surgical_history = models.TextField(_('التاريخ الجراحي'), blank=True)
    lifestyle = models.TextField(_('نمط الحياة'), blank=True)
    occupation = models.CharField(_('المهنة'), max_length=100, blank=True)
    smoking_status = models.CharField(
        _('حالة التدخين'),
        max_length=20,
        choices=(
            ('never', _('لا يدخن')),
            ('former', _('مدخن سابق')),
            ('current', _('مدخن حالي'))
        ),
        blank=True
    )
    alcohol_consumption = models.CharField(
        _('استهلاك الكحول'),
        max_length=20,
        choices=(
            ('never', _('لا يشرب')),
            ('occasional', _('نادراً')),
            ('moderate', _('معتدل')),
            ('heavy', _('كثير'))
        ),
        blank=True
    )
    
    class Meta:
        verbose_name = _('تاريخ طبي')
        verbose_name_plural = _('التواريخ الطبية')
    
    def __str__(self):
        return f"التاريخ الطبي - {self.patient}"


class Allergy(TimestampMixin):
    """
    Patient allergy information
    """
    SEVERITY_CHOICES = (
        ('mild', _('خفيف')),
        ('moderate', _('متوسط')),
        ('severe', _('شديد')),
        ('life_threatening', _('مهدد للحياة'))
    )
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='allergies',
        verbose_name=_('المريض')
    )
    allergen = models.CharField(_('المسبب'), max_length=100)
    allergy_type = models.CharField(
        _('نوع الحساسية'),
        max_length=50,
        choices=(
            ('food', _('طعام')),
            ('medication', _('دواء')),
            ('environmental', _('بيئي')),
            ('other', _('آخر'))
        )
    )
    severity = models.CharField(
        _('شدة الحساسية'),
        max_length=20,
        choices=SEVERITY_CHOICES
    )
    reaction = models.TextField(_('رد الفعل'))
    diagnosis_date = models.DateField(_('تاريخ التشخيص'))
    notes = models.TextField(_('ملاحظات'), blank=True)
    
    class Meta:
        verbose_name = _('حساسية')
        verbose_name_plural = _('الحساسيات')
        ordering = ['-diagnosis_date']
    
    def __str__(self):
        return f"{self.patient} - {self.allergen}"


class ChronicCondition(TimestampMixin):
    """
    Patient chronic conditions
    """
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='chronic_conditions',
        verbose_name=_('المريض')
    )
    condition_name = models.CharField(_('اسم الحالة'), max_length=100)
    diagnosis_date = models.DateField(_('تاريخ التشخيص'))
    severity = models.CharField(
        _('شدة الحالة'),
        max_length=20,
        choices=(
            ('mild', _('خفيف')),
            ('moderate', _('متوسط')),
            ('severe', _('شديد'))
        )
    )
    status = models.CharField(
        _('الحالة'),
        max_length=20,
        choices=(
            ('active', _('نشط')),
            ('controlled', _('متحكم به')),
            ('in_remission', _('في تحسن')),
            ('resolved', _('تم الشفاء'))
        )
    )
    treating_doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        related_name='treated_conditions',
        verbose_name=_('الطبيب المعالج')
    )
    treatment_plan = models.TextField(_('خطة العلاج'))
    notes = models.TextField(_('ملاحظات'), blank=True)
    
    class Meta:
        verbose_name = _('حالة مزمنة')
        verbose_name_plural = _('الحالات المزمنة')
        ordering = ['-diagnosis_date']
    
    def __str__(self):
        return f"{self.patient} - {self.condition_name}"


class Vaccination(TimestampMixin):
    """
    Patient vaccination records
    """
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='vaccinations',
        verbose_name=_('المريض')
    )
    vaccine_name = models.CharField(_('اسم اللقاح'), max_length=100)
    dose_number = models.PositiveIntegerField(_('رقم الجرعة'))
    administration_date = models.DateField(_('تاريخ الإعطاء'))
    administered_by = models.CharField(_('تم الإعطاء بواسطة'), max_length=100)
    lot_number = models.CharField(_('رقم التشغيلة'), max_length=50, blank=True)
    manufacturer = models.CharField(_('الشركة المصنعة'), max_length=100)
    next_due_date = models.DateField(
        _('تاريخ الجرعة القادمة'),
        null=True,
        blank=True
    )
    side_effects = models.TextField(_('الآثار الجانبية'), blank=True)
    notes = models.TextField(_('ملاحظات'), blank=True)
    
    class Meta:
        verbose_name = _('تطعيم')
        verbose_name_plural = _('التطعيمات')
        ordering = ['-administration_date']
        unique_together = ['patient', 'vaccine_name', 'dose_number']
    
    def __str__(self):
        return f"{self.patient} - {self.vaccine_name} (الجرعة {self.dose_number})"


class MedicalDocument(TimestampMixin):
    """
    Medical documents and reports
    """
    DOCUMENT_TYPES = (
        ('lab_report', _('تقرير مخبري')),
        ('radiology', _('صور أشعة')),
        ('prescription', _('وصفة طبية')),
        ('discharge_summary', _('ملخص خروج')),
        ('referral', _('تحويل طبي')),
        ('other', _('آخر'))
    )
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='medical_documents',
        verbose_name=_('المريض')
    )
    document_type = models.CharField(
        _('نوع الوثيقة'),
        max_length=20,
        choices=DOCUMENT_TYPES
    )
    title = models.CharField(_('العنوان'), max_length=200)
    description = models.TextField(_('الوصف'), blank=True)
    file = models.FileField(_('الملف'), upload_to='medical_documents/')
    uploaded_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_documents',
        verbose_name=_('تم الرفع بواسطة')
    )
    document_date = models.DateField(_('تاريخ الوثيقة'))
    is_confidential = models.BooleanField(_('سري'), default=False)
    tags = models.CharField(_('الوسوم'), max_length=200, blank=True)
    
    class Meta:
        verbose_name = _('وثيقة طبية')
        verbose_name_plural = _('الوثائق الطبية')
        ordering = ['-document_date']
    
    def __str__(self):
        return f"{self.patient} - {self.title}"
