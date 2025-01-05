from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User

class MedicalRecord(models.Model):
    """السجل الطبي"""
    
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='patient_records',
        verbose_name=_('المريض')
    )
    
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='doctor_records',
        verbose_name=_('الطبيب')
    )
    
    diagnosis = models.TextField(
        verbose_name=_('التشخيص')
    )
    
    treatment = models.TextField(
        verbose_name=_('العلاج')
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name=_('ملاحظات')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('تاريخ التحديث')
    )
    
    def __str__(self):
        return f"سجل {self.patient.get_full_name()} - {self.created_at.date()}"

    class Meta:
        verbose_name = _('سجل طبي')
        verbose_name_plural = _('سجلات طبية')
        ordering = ['-created_at']

class VitalSigns(models.Model):
    """العلامات الحيوية"""
    
    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name='vital_signs',
        verbose_name=_('السجل الطبي')
    )
    
    temperature = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        verbose_name=_('درجة الحرارة')
    )
    
    blood_pressure_systolic = models.IntegerField(
        verbose_name=_('ضغط الدم الانقباضي')
    )
    
    blood_pressure_diastolic = models.IntegerField(
        verbose_name=_('ضغط الدم الانبساطي')
    )
    
    heart_rate = models.IntegerField(
        verbose_name=_('معدل ضربات القلب')
    )
    
    respiratory_rate = models.IntegerField(
        verbose_name=_('معدل التنفس')
    )
    
    oxygen_saturation = models.IntegerField(
        verbose_name=_('تشبع الأكسجين')
    )
    
    recorded_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_('سجل بواسطة')
    )
    
    recorded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ التسجيل')
    )
    
    class Meta:
        verbose_name = _('علامات حيوية')
        verbose_name_plural = _('العلامات الحيوية')
        ordering = ['-recorded_at']

class Prescription(models.Model):
    """الوصفة الطبية"""
    
    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name='prescriptions',
        verbose_name=_('السجل الطبي')
    )
    
    medication = models.CharField(
        max_length=200,
        verbose_name=_('الدواء')
    )
    
    dosage = models.CharField(
        max_length=100,
        verbose_name=_('الجرعة')
    )
    
    frequency = models.CharField(
        max_length=100,
        verbose_name=_('التكرار')
    )
    
    duration = models.CharField(
        max_length=100,
        verbose_name=_('المدة')
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name=_('ملاحظات')
    )
    
    prescribed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='prescriptions',
        verbose_name=_('وصف بواسطة')
    )
    
    prescribed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الوصف')
    )
    
    filled = models.BooleanField(
        default=False,
        verbose_name=_('تم صرفه')
    )
    
    filled_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='filled_prescriptions',
        verbose_name=_('صرف بواسطة')
    )
    
    filled_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('تاريخ الصرف')
    )
    
    def __str__(self):
        return f"وصفة {self.medication} - {self.medical_record.patient.get_full_name()}"

    class Meta:
        verbose_name = _('وصفة طبية')
        verbose_name_plural = _('الوصفات الطبية')
        ordering = ['-prescribed_at']

class LabTest(models.Model):
    """فحص مخبري"""
    
    STATUS_CHOICES = [
        ('pending', _('قيد الانتظار')),
        ('completed', _('مكتمل')),
        ('cancelled', _('ملغي')),
    ]

    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name='lab_tests',
        verbose_name=_('السجل الطبي')
    )
    
    test_name = models.CharField(
        max_length=200,
        verbose_name=_('اسم الفحص')
    )
    
    test_date = models.DateTimeField(
        verbose_name=_('تاريخ الفحص')
    )
    
    results = models.TextField(
        blank=True,
        verbose_name=_('النتائج')
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('الحالة')
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name=_('ملاحظات')
    )
    
    def __str__(self):
        return f"فحص {self.test_name} - {self.medical_record.patient.get_full_name()}"

    class Meta:
        verbose_name = _('فحص مخبري')
        verbose_name_plural = _('فحوصات مخبرية')
        ordering = ['-test_date']

class LabResult(models.Model):
    """نتائج المختبر"""
    
    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name='lab_results',
        verbose_name=_('السجل الطبي')
    )
    
    test_name = models.CharField(
        max_length=100,
        verbose_name=_('اسم الفحص')
    )
    
    result = models.TextField(
        verbose_name=_('النتيجة')
    )
    
    normal_range = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('المعدل الطبيعي')
    )
    
    unit = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('الوحدة')
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name=_('ملاحظات')
    )
    
    performed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='lab_results',
        verbose_name=_('أجري بواسطة')
    )
    
    performed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإجراء')
    )
    
    class Meta:
        verbose_name = _('نتيجة مختبر')
        verbose_name_plural = _('نتائج المختبر')
        ordering = ['-performed_at']
