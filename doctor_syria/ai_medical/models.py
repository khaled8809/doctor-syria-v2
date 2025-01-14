from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from medical_records.models import MedicalRecord

from accounts.models import Doctor, Patient


class AIModel(models.Model):
    """نماذج الذكاء الاصطناعي"""

    MODEL_TYPES = [
        ("diagnosis", "تشخيص"),
        ("prognosis", "تنبؤ"),
        ("risk_assessment", "تقييم المخاطر"),
        ("image_analysis", "تحليل الصور"),
        ("drug_interaction", "تفاعلات الأدوية"),
        ("genetic_analysis", "تحليل جيني"),
    ]

    name = models.CharField(max_length=200)
    model_type = models.CharField(max_length=20, choices=MODEL_TYPES)
    version = models.CharField(max_length=50)
    description = models.TextField()
    input_parameters = models.JSONField()
    output_format = models.JSONField()
    accuracy = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    last_trained = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} v{self.version}"


class DiagnosisRequest(models.Model):
    """طلبات التشخيص"""

    STATUS_CHOICES = [
        ("pending", "قيد الانتظار"),
        ("processing", "قيد المعالجة"),
        ("completed", "مكتمل"),
        ("failed", "فشل"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    requesting_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    ai_model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    symptoms = models.JSONField()
    medical_history = models.JSONField()
    vital_signs = models.JSONField()
    lab_results = models.JSONField(null=True, blank=True)
    images = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"طلب تشخيص - {self.patient.user.get_full_name()}"


class DiagnosisResult(models.Model):
    """نتائج التشخيص"""

    request = models.OneToOneField(DiagnosisRequest, on_delete=models.CASCADE)
    diagnoses = models.JSONField()  # قائمة التشخيصات مع نسب الاحتمالية
    confidence_score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    supporting_evidence = models.JSONField()
    recommendations = models.JSONField()
    warnings = models.JSONField(default=list)
    processing_time = models.DurationField()
    reviewed_by = models.ForeignKey(
        Doctor, on_delete=models.SET_NULL, null=True, blank=True
    )
    review_notes = models.TextField(blank=True)

    def __str__(self):
        return f"نتيجة تشخيص - {self.request.patient.user.get_full_name()}"


class RiskAssessment(models.Model):
    """تقييم المخاطر"""

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    ai_model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    risk_factors = models.JSONField()
    assessment_date = models.DateField()
    risk_scores = models.JSONField()  # درجات المخاطر لمختلف الأمراض
    recommendations = models.JSONField()
    next_assessment_date = models.DateField()
    created_by = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"تقييم مخاطر - {self.patient.user.get_full_name()}"


class ImageAnalysis(models.Model):
    """تحليل الصور الطبية"""

    IMAGE_TYPES = [
        ("xray", "أشعة سينية"),
        ("ct", "أشعة مقطعية"),
        ("mri", "رنين مغناطيسي"),
        ("ultrasound", "موجات صوتية"),
        ("pathology", "أنسجة"),
        ("dermatology", "جلدية"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    ai_model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPES)
    image_file = models.ImageField(upload_to="ai_analysis/")
    analysis_results = models.JSONField()
    annotations = models.JSONField(default=dict)
    confidence_scores = models.JSONField()
    processing_time = models.DurationField()
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"تحليل صورة {self.get_image_type_display()} - {self.patient.user.get_full_name()}"


class DrugInteractionCheck(models.Model):
    """فحص تفاعلات الأدوية"""

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    ai_model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    medications = models.JSONField()
    conditions = models.JSONField()
    allergies = models.JSONField(default=list)
    interactions_found = models.JSONField()
    severity_levels = models.JSONField()
    recommendations = models.JSONField()
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"فحص تفاعلات الأدوية - {self.patient.user.get_full_name()}"


class TreatmentOptimization(models.Model):
    """تحسين العلاج"""

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    ai_model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    current_treatment = models.JSONField()
    patient_factors = models.JSONField()
    optimization_results = models.JSONField()
    expected_outcomes = models.JSONField()
    cost_benefit_analysis = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"تحسين علاج - {self.patient.user.get_full_name()}"


class PredictiveAlert(models.Model):
    """التنبيهات التنبؤية"""

    SEVERITY_LEVELS = [
        ("low", "منخفض"),
        ("medium", "متوسط"),
        ("high", "عالي"),
        ("critical", "حرج"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    ai_model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=100)
    prediction = models.JSONField()
    confidence_score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    recommended_actions = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"تنبيه تنبؤي - {self.patient.user.get_full_name()}"


class ModelPerformanceMetric(models.Model):
    """مقاييس أداء النموذج"""

    ai_model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    metric_name = models.CharField(max_length=100)
    metric_value = models.FloatField()
    measurement_date = models.DateTimeField()
    sample_size = models.IntegerField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.metric_name} - {self.ai_model.name}"
