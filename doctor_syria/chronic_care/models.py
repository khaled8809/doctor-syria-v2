from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from medical_records.models import MedicalRecord

from accounts.models import Doctor, Patient


class ChronicCondition(models.Model):
    """الأمراض المزمنة"""

    SEVERITY_LEVELS = [
        ("mild", "خفيف"),
        ("moderate", "متوسط"),
        ("severe", "شديد"),
        ("critical", "حرج"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    condition_name = models.CharField(max_length=200)
    diagnosis_date = models.DateField()
    diagnosing_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    description = models.TextField()
    symptoms = models.JSONField(default=list)
    risk_factors = models.JSONField(default=list)
    complications = models.JSONField(default=list)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.condition_name} - {self.patient.user.get_full_name()}"


class CareTeam(models.Model):
    """فريق الرعاية"""

    ROLE_CHOICES = [
        ("primary", "طبيب رئيسي"),
        ("specialist", "طبيب مختص"),
        ("nurse", "ممرض"),
        ("nutritionist", "أخصائي تغذية"),
        ("physical_therapist", "معالج طبيعي"),
        ("coordinator", "منسق رعاية"),
    ]

    condition = models.ForeignKey(ChronicCondition, on_delete=models.CASCADE)
    member = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_role_display()} - {self.condition.condition_name}"


class CarePlan(models.Model):
    """خطة الرعاية"""

    STATUS_CHOICES = [
        ("active", "نشطة"),
        ("completed", "مكتملة"),
        ("suspended", "موقوفة"),
        ("discontinued", "متوقفة"),
    ]

    condition = models.ForeignKey(ChronicCondition, on_delete=models.CASCADE)
    created_by = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    goals = models.JSONField()
    interventions = models.JSONField()
    medications = models.JSONField()
    lifestyle_modifications = models.JSONField()
    monitoring_parameters = models.JSONField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    review_frequency = models.CharField(max_length=50)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"خطة رعاية - {self.condition.condition_name}"


class HealthMonitoring(models.Model):
    """مراقبة المؤشرات الصحية"""

    condition = models.ForeignKey(ChronicCondition, on_delete=models.CASCADE)
    parameter_name = models.CharField(max_length=100)
    value = models.FloatField()
    unit = models.CharField(max_length=50)
    measured_at = models.DateTimeField()
    measured_by = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    is_normal = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.parameter_name} - {self.condition.patient.user.get_full_name()}"


class Medication(models.Model):
    """الأدوية"""

    FREQUENCY_CHOICES = [
        ("daily", "يومياً"),
        ("twice_daily", "مرتين يومياً"),
        ("thrice_daily", "ثلاث مرات يومياً"),
        ("weekly", "أسبوعياً"),
        ("monthly", "شهرياً"),
        ("as_needed", "عند الحاجة"),
    ]

    condition = models.ForeignKey(ChronicCondition, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    instructions = models.TextField()
    side_effects = models.JSONField(default=list)
    interactions = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.condition.patient.user.get_full_name()}"


class ProgressUpdate(models.Model):
    """تحديثات التقدم"""

    condition = models.ForeignKey(ChronicCondition, on_delete=models.CASCADE)
    date = models.DateField()
    symptoms_status = models.JSONField()
    improvements = models.TextField()
    challenges = models.TextField()
    medication_adherence = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    lifestyle_adherence = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"تحديث - {self.condition.condition_name} - {self.date}"


class FollowUp(models.Model):
    """متابعة الحالة"""

    STATUS_CHOICES = [
        ("scheduled", "مجدولة"),
        ("completed", "مكتملة"),
        ("cancelled", "ملغية"),
        ("rescheduled", "معاد جدولتها"),
    ]

    condition = models.ForeignKey(ChronicCondition, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    scheduled_date = models.DateTimeField()
    actual_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="scheduled"
    )
    findings = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    next_appointment = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"متابعة - {self.condition.condition_name} - {self.scheduled_date}"


class EducationalResource(models.Model):
    """الموارد التثقيفية"""

    RESOURCE_TYPES = [
        ("article", "مقال"),
        ("video", "فيديو"),
        ("pdf", "ملف PDF"),
        ("infographic", "انفوجرافيك"),
        ("webinar", "ندوة عبر الإنترنت"),
    ]

    condition = models.ForeignKey(ChronicCondition, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    content = models.TextField()
    file = models.FileField(upload_to="educational_resources/", null=True, blank=True)
    url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class EmergencyPlan(models.Model):
    """خطة الطوارئ"""

    condition = models.OneToOneField(ChronicCondition, on_delete=models.CASCADE)
    warning_signs = models.JSONField()
    emergency_contacts = models.JSONField()
    immediate_actions = models.TextField()
    hospital_preference = models.CharField(max_length=200)
    medications_list = models.JSONField()
    allergies = models.JSONField(default=list)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"خطة طوارئ - {self.condition.condition_name}"


class LifestyleLog(models.Model):
    """سجل نمط الحياة"""

    condition = models.ForeignKey(ChronicCondition, on_delete=models.CASCADE)
    date = models.DateField()
    exercise_minutes = models.IntegerField()
    sleep_hours = models.FloatField()
    stress_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    diet_adherence = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"سجل نمط الحياة - {self.condition.patient.user.get_full_name()} - {self.date}"
