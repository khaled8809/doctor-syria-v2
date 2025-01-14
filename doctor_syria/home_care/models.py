from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from medical_records.models import MedicalRecord

from accounts.models import Doctor, Nurse, Patient


class CareProvider(models.Model):
    """مقدمي الرعاية المنزلية"""

    PROVIDER_TYPES = [
        ("nurse", "ممرض/ة"),
        ("physiotherapist", "معالج طبيعي"),
        ("occupational_therapist", "معالج وظيفي"),
        ("caregiver", "مقدم رعاية"),
        ("nutritionist", "أخصائي تغذية"),
    ]

    user = models.OneToOneField("accounts.User", on_delete=models.CASCADE)
    provider_type = models.CharField(max_length=50, choices=PROVIDER_TYPES)
    specialization = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField()
    availability = models.JSONField(default=dict)  # ساعات العمل المتاحة
    service_area = models.TextField(help_text="المناطق التي يخدمها")
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], default=0
    )

    def __str__(self):
        return f"{self.get_provider_type_display()} - {self.user.get_full_name()}"


class HomeCareService(models.Model):
    """خدمات الرعاية المنزلية"""

    name = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.DurationField(help_text="المدة المتوقعة للخدمة")
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    required_provider_type = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CareRequest(models.Model):
    """طلبات الرعاية المنزلية"""

    STATUS_CHOICES = [
        ("pending", "قيد الانتظار"),
        ("approved", "موافق عليه"),
        ("in_progress", "قيد التنفيذ"),
        ("completed", "مكتمل"),
        ("cancelled", "ملغي"),
    ]

    URGENCY_LEVELS = [
        ("low", "منخفض"),
        ("medium", "متوسط"),
        ("high", "عالي"),
        ("urgent", "عاجل"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    service = models.ForeignKey(HomeCareService, on_delete=models.CASCADE)
    provider = models.ForeignKey(CareProvider, on_delete=models.SET_NULL, null=True)
    supervising_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    visit_frequency = models.CharField(max_length=50)
    preferred_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    urgency_level = models.CharField(max_length=20, choices=URGENCY_LEVELS)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"طلب رعاية - {self.patient.user.get_full_name()}"


class CareVisit(models.Model):
    """زيارات الرعاية المنزلية"""

    STATUS_CHOICES = [
        ("scheduled", "مجدولة"),
        ("in_progress", "جارية"),
        ("completed", "مكتملة"),
        ("cancelled", "ملغية"),
        ("missed", "متغيب عنها"),
    ]

    care_request = models.ForeignKey(CareRequest, on_delete=models.CASCADE)
    provider = models.ForeignKey(CareProvider, on_delete=models.CASCADE)
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="scheduled"
    )
    notes = models.TextField(blank=True)
    signature = models.ImageField(upload_to="visit_signatures/", null=True, blank=True)

    def __str__(self):
        return f"زيارة {self.scheduled_date} - {self.care_request.patient.user.get_full_name()}"


class CareTask(models.Model):
    """مهام الرعاية"""

    visit = models.ForeignKey(CareVisit, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=200)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.task_name} - {self.visit}"


class VitalSignRecord(models.Model):
    """سجلات العلامات الحيوية"""

    visit = models.ForeignKey(CareVisit, on_delete=models.CASCADE)
    vital_sign = models.ForeignKey(
        "medical_records.VitalSigns", on_delete=models.CASCADE
    )
    value = models.JSONField()
    measured_at = models.DateTimeField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.vital_sign} - {self.visit}"


class CareReport(models.Model):
    """تقارير الرعاية"""

    visit = models.OneToOneField(CareVisit, on_delete=models.CASCADE)
    content = models.TextField()
    medications_given = models.JSONField(default=list)
    complications = models.TextField(blank=True)
    recommendations = models.TextField()
    next_visit_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"تقرير زيارة {self.visit.scheduled_date}"


class CareReview(models.Model):
    """تقييمات الرعاية"""

    visit = models.OneToOneField(CareVisit, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False)

    def __str__(self):
        return f"تقييم زيارة {self.visit.scheduled_date}"


class EmergencyContact(models.Model):
    """جهات الاتصال في حالات الطوارئ"""

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    alternative_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField()
    is_primary = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return (
            f"{self.name} - {self.relationship} لـ {self.patient.user.get_full_name()}"
        )
