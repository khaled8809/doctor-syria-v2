from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import Patient, Doctor
from django.utils.translation import gettext_lazy as _
from core.models import TimestampMixin, SoftDeleteMixin, AuditMixin
from .choices import (
    AppointmentStatus, AppointmentType, RecordType, Severity,
    AllergyType, AllergyReaction, VaccinationType
)

class MedicalRecord(TimestampMixin, SoftDeleteMixin, AuditMixin):
    """الملف الطبي الأساسي"""
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=5, choices=[
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ])
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text="بالسنتيمتر")
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="بالكيلوغرام")
    allergies = models.TextField(blank=True)
    chronic_conditions = models.TextField(blank=True)
    family_history = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100)
    emergency_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    doctor = models.ForeignKey(
        Doctor, on_delete=models.PROTECT,
        related_name='doctor_records',
        verbose_name=_('الطبيب')
    )
    record_type = models.CharField(
        _('نوع السجل'),
        max_length=20,
        choices=RecordType.choices
    )
    title = models.CharField(_('العنوان'), max_length=200)
    description = models.TextField(_('الوصف'))
    date = models.DateTimeField(_('التاريخ'), default=timezone.now)
    severity = models.CharField(
        _('مستوى الخطورة'),
        max_length=10,
        choices=Severity.choices,
        default=Severity.LOW
    )
    notes = models.TextField(_('ملاحظات'), blank=True)
    attachments = models.FileField(
        _('المرفقات'),
        upload_to='medical_records/',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('سجل طبي')
        verbose_name_plural = _('السجلات الطبية')
        ordering = ['-date']

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
    blood_pressure_systolic = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(300)])
    blood_pressure_diastolic = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    heart_rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(250)])
    temperature = models.DecimalField(max_digits=4, decimal_places=1)
    blood_sugar = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)])
    oxygen_saturation = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"مؤشرات {self.patient.user.get_full_name()} في {self.date}"

class Medication(models.Model):
    """الأدوية والجرعات"""
    FREQUENCY_CHOICES = [
        ('daily', 'يومياً'),
        ('twice_daily', 'مرتين يومياً'),
        ('three_times', 'ثلاث مرات يومياً'),
        ('four_times', 'أربع مرات يومياً'),
        ('weekly', 'أسبوعياً'),
        ('monthly', 'شهرياً'),
        ('as_needed', 'عند الحاجة'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'نشط'),
        ('completed', 'مكتمل'),
        ('discontinued', 'متوقف'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    prescribing_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.patient.user.get_full_name()}"

    @property
    def is_active(self):
        return self.status == 'active' and (not self.end_date or self.end_date >= timezone.now().date())

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
        ('scheduled', 'مجدول'),
        ('confirmed', 'مؤكد'),
        ('completed', 'مكتمل'),
        ('cancelled', 'ملغي'),
        ('no_show', 'لم يحضر'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_type = models.CharField(
        _('نوع الموعد'),
        max_length=20,
        choices=AppointmentType.choices
    )
    status = models.CharField(
        _('حالة الموعد'),
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.PENDING
    )
    scheduled_time = models.DateTimeField(_('وقت الموعد'))
    duration = models.PositiveIntegerField(
        _('المدة (بالدقائق)'),
        default=30,
        validators=[MinValueValidator(15), MaxValueValidator(180)]
    )
    reason = models.TextField(_('سبب الزيارة'))
    notes = models.TextField(_('ملاحظات'), blank=True)
    cancellation_reason = models.TextField(_('سبب الإلغاء'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('موعد')
        verbose_name_plural = _('المواعيد')
        ordering = ['-scheduled_time']
        indexes = [
            models.Index(fields=['doctor', 'scheduled_time']),
            models.Index(fields=['patient', 'scheduled_time']),
            models.Index(fields=['status', 'scheduled_time']),
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
        ('weight', 'الوزن'),
        ('exercise', 'التمارين'),
        ('diet', 'النظام الغذائي'),
        ('blood_pressure', 'ضغط الدم'),
        ('blood_sugar', 'سكر الدم'),
        ('other', 'أخرى'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_value = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
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
        ordering = ['-date']

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
    file = models.FileField(upload_to='lab_results/', null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-test_date']

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
        ordering = ['-date_given']

    def __str__(self):
        return f"{self.vaccine_name} - {self.patient.user.get_full_name()}"

class Prescription(TimestampMixin, SoftDeleteMixin, AuditMixin):
    """
    الوصفات الطبية
    """
    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.PROTECT,
        related_name='prescriptions',
        verbose_name=_('السجل الطبي')
    )
    medicine_name = models.CharField(_('اسم الدواء'), max_length=200)
    dosage = models.CharField(_('الجرعة'), max_length=100)
    frequency = models.CharField(_('عدد مرات الأخذ'), max_length=100)
    duration = models.CharField(_('مدة العلاج'), max_length=100)
    instructions = models.TextField(_('تعليمات'), blank=True)
    is_chronic = models.BooleanField(_('دواء مزمن'), default=False)
    refills = models.PositiveIntegerField(_('عدد مرات إعادة الصرف'), default=0)
    notes = models.TextField(_('ملاحظات'), blank=True)

    class Meta:
        verbose_name = _('وصفة طبية')
        verbose_name_plural = _('الوصفات الطبية')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.medicine_name} - {self.medical_record.patient.user.get_full_name()}"

class Allergy(TimestampMixin, SoftDeleteMixin, AuditMixin):
    """
    الحساسية
    """
    patient = models.ForeignKey(
        'accounts.User', on_delete=models.PROTECT,
        related_name='patient_allergies',
        limit_choices_to={'user_type': 'patient'},
        verbose_name=_('المريض')
    )
    allergy_type = models.CharField(
        _('نوع الحساسية'),
        max_length=20,
        choices=AllergyType.choices
    )
    allergen = models.CharField(_('المسبب'), max_length=200)
    reaction = models.CharField(
        _('رد الفعل'),
        max_length=20,
        choices=AllergyReaction.choices
    )
    diagnosis_date = models.DateField(_('تاريخ التشخيص'))
    notes = models.TextField(_('ملاحظات'), blank=True)

    class Meta:
        verbose_name = _('حساسية')
        verbose_name_plural = _('الحساسيات')
        ordering = ['-diagnosis_date']
        unique_together = ['patient', 'allergen']

    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.allergen}"

class AllergyReaction(models.Model):
    """
    ردود أفعال الحساسية
    """
    allergy = models.ForeignKey(
        Allergy, on_delete=models.CASCADE,
        related_name='reactions',
        verbose_name=_('الحساسية')
    )
    reaction = models.CharField(_('رد الفعل'), max_length=200)
    notes = models.TextField(_('ملاحظات'), blank=True)

    def __str__(self):
        return f"{self.allergy.patient.user.get_full_name()} - {self.reaction}"

class Vaccination(TimestampMixin, SoftDeleteMixin, AuditMixin):
    """
    التطعيمات
    """
    patient = models.ForeignKey(
        'accounts.User', on_delete=models.PROTECT,
        related_name='patient_vaccinations',
        limit_choices_to={'user_type': 'patient'},
        verbose_name=_('المريض')
    )
    vaccine_type = models.CharField(
        _('نوع التطعيم'),
        max_length=20,
        choices=VaccinationType.choices
    )
    vaccine_name = models.CharField(_('اسم التطعيم'), max_length=200)
    dose_number = models.PositiveIntegerField(_('رقم الجرعة'), default=1)
    date_given = models.DateField(_('تاريخ الأخذ'))
    given_by = models.ForeignKey(
        Doctor, on_delete=models.PROTECT,
        related_name='administered_vaccinations',
        verbose_name=_('الطبيب المعطي')
    )
    next_dose_date = models.DateField(_('تاريخ الجرعة القادمة'), null=True, blank=True)
    batch_number = models.CharField(_('رقم التشغيلة'), max_length=50, blank=True)
    manufacturer = models.CharField(_('الشركة المصنعة'), max_length=200, blank=True)
    notes = models.TextField(_('ملاحظات'), blank=True)

    class Meta:
        verbose_name = _('تطعيم')
        verbose_name_plural = _('التطعيمات')
        ordering = ['-date_given']
        unique_together = ['patient', 'vaccine_type', 'dose_number']

    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.vaccine_name} - الجرعة {self.dose_number}"
