from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from medical_records.models import MedicalRecord

from accounts.models import Doctor, Hospital, Patient


class RadiologyCenter(models.Model):
    """مراكز الأشعة"""

    name = models.CharField(max_length=200)
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, null=True, blank=True
    )
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    working_hours = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    equipment = models.JSONField(default=list)  # قائمة المعدات المتوفرة
    accreditation = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ImagingService(models.Model):
    """خدمات التصوير الطبي"""

    MODALITY_TYPES = [
        ("xray", "أشعة سينية"),
        ("ct", "أشعة مقطعية"),
        ("mri", "رنين مغناطيسي"),
        ("ultrasound", "موجات صوتية"),
        ("mammogram", "تصوير الثدي"),
        ("dexa", "قياس كثافة العظام"),
        ("pet", "تصوير المقطع البوزيتروني"),
    ]

    center = models.ForeignKey(RadiologyCenter, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    modality = models.CharField(max_length=20, choices=MODALITY_TYPES)
    description = models.TextField()
    preparation_instructions = models.TextField()
    duration = models.DurationField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_modality_display()} - {self.name}"


class ImagingAppointment(models.Model):
    """مواعيد التصوير"""

    STATUS_CHOICES = [
        ("scheduled", "مجدول"),
        ("confirmed", "مؤكد"),
        ("in_progress", "قيد التنفيذ"),
        ("completed", "مكتمل"),
        ("cancelled", "ملغي"),
        ("no_show", "لم يحضر"),
    ]

    PRIORITY_LEVELS = [
        ("routine", "روتيني"),
        ("urgent", "عاجل"),
        ("emergency", "طارئ"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    service = models.ForeignKey(ImagingService, on_delete=models.CASCADE)
    referring_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="scheduled"
    )
    priority = models.CharField(
        max_length=20, choices=PRIORITY_LEVELS, default="routine"
    )
    clinical_notes = models.TextField()
    special_instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.name} - {self.patient.user.get_full_name()}"


class ImagingStudy(models.Model):
    """دراسات التصوير"""

    appointment = models.OneToOneField(ImagingAppointment, on_delete=models.CASCADE)
    study_uid = models.CharField(max_length=100, unique=True)
    performed_by = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    radiation_dose = models.FloatField(null=True, blank=True)
    contrast_used = models.BooleanField(default=False)
    contrast_details = models.TextField(blank=True)
    complications = models.TextField(blank=True)
    technical_notes = models.TextField(blank=True)

    def __str__(self):
        return f"دراسة {self.study_uid}"

    class Meta:
        verbose_name_plural = "Imaging Studies"


class ImagingSeries(models.Model):
    """سلسلة الصور"""

    study = models.ForeignKey(ImagingStudy, on_delete=models.CASCADE)
    series_uid = models.CharField(max_length=100, unique=True)
    series_number = models.IntegerField()
    modality = models.CharField(max_length=20)
    body_part = models.CharField(max_length=100)
    protocol = models.CharField(max_length=200)
    number_of_images = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"سلسلة {self.series_uid}"

    class Meta:
        verbose_name_plural = "Imaging Series"


class Image(models.Model):
    """الصور الطبية"""

    series = models.ForeignKey(ImagingSeries, on_delete=models.CASCADE)
    image_uid = models.CharField(max_length=100, unique=True)
    image_number = models.IntegerField()
    file = models.FileField(upload_to="medical_images/")
    thumbnail = models.ImageField(upload_to="image_thumbnails/", null=True)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"صورة {self.image_uid}"


class RadiologyReport(models.Model):
    """تقارير الأشعة"""

    STATUS_CHOICES = [
        ("draft", "مسودة"),
        ("preliminary", "أولي"),
        ("final", "نهائي"),
        ("amended", "معدل"),
    ]

    study = models.OneToOneField(ImagingStudy, on_delete=models.CASCADE)
    radiologist = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    findings = models.TextField()
    impression = models.TextField()
    recommendations = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    finalized_at = models.DateTimeField(null=True, blank=True)
    amended_at = models.DateTimeField(null=True, blank=True)
    amendment_reason = models.TextField(blank=True)

    def __str__(self):
        return f"تقرير {self.study.study_uid}"


class AIAnalysis(models.Model):
    """تحليل الذكاء الاصطناعي"""

    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    algorithm_name = models.CharField(max_length=100)
    algorithm_version = models.CharField(max_length=50)
    analysis_result = models.JSONField()
    confidence_score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    processing_time = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"تحليل {self.algorithm_name} للصورة {self.image.image_uid}"

    class Meta:
        verbose_name_plural = "AI Analyses"
