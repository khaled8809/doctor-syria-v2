from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from doctors.models import Doctor

from patient_records.models import MedicalRecord, Patient
from saas_core.models import Tenant


class Symptom(models.Model):
    """نموذج الأعراض المرضية"""

    name = models.CharField(max_length=200)
    description = models.TextField()
    severity_level = models.IntegerField(
        choices=[
            (1, "خفيف"),
            (2, "متوسط"),
            (3, "شديد"),
        ]
    )
    keywords = models.JSONField(help_text="الكلمات المفتاحية المرتبطة بالعرض")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Disease(models.Model):
    """نموذج الأمراض"""

    name = models.CharField(max_length=200)
    description = models.TextField()
    symptoms = models.ManyToManyField(Symptom, through="DiseaseSymptom")
    icd_code = models.CharField(max_length=20, help_text="رمز التصنيف الدولي للأمراض")
    risk_level = models.IntegerField(
        choices=[
            (1, "منخفض"),
            (2, "متوسط"),
            (3, "مرتفع"),
        ]
    )
    common_treatments = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.icd_code})"


class DiseaseSymptom(models.Model):
    """نموذج العلاقة بين المرض والأعراض"""

    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    probability = models.FloatField(help_text="احتمالية ظهور العرض مع المرض")
    importance = models.IntegerField(help_text="أهمية العرض في تشخيص المرض")

    class Meta:
        unique_together = ["disease", "symptom"]


class AIModel(models.Model):
    """نموذج نماذج الذكاء الاصطناعي"""

    MODEL_TYPES = [
        ("DIAGNOSIS", "تشخيص"),
        ("PREDICTION", "تنبؤ"),
        ("ANALYSIS", "تحليل"),
    ]

    name = models.CharField(max_length=100)
    model_type = models.CharField(max_length=20, choices=MODEL_TYPES)
    version = models.CharField(max_length=20)
    description = models.TextField()
    model_file = models.FileField(upload_to="ai_models/")
    accuracy = models.FloatField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} v{self.version}"


class DiagnosisSession(models.Model):
    """نموذج جلسة التشخيص"""

    STATUS_CHOICES = [
        ("ACTIVE", "نشط"),
        ("COMPLETED", "مكتمل"),
        ("CANCELLED", "ملغي"),
    ]

    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='diagnosis_sessions'
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    ai_model = models.ForeignKey(AIModel, on_delete=models.PROTECT)
    symptoms = models.ManyToManyField(Symptom, through="SessionSymptom")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"جلسة {self.patient.name} - {self.start_time}"


class SessionSymptom(models.Model):
    """نموذج أعراض الجلسة"""

    session = models.ForeignKey(DiagnosisSession, on_delete=models.CASCADE)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    severity = models.IntegerField(choices=Symptom.severity_level.field.choices)
    notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)


class DiagnosisResult(models.Model):
    """نموذج نتائج التشخيص"""

    session = models.ForeignKey(DiagnosisSession, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    confidence = models.FloatField(help_text="نسبة الثقة في التشخيص")
    reasoning = models.JSONField(help_text="تفسير التشخيص")
    recommendations = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"تشخيص {self.disease.name} ({self.confidence}%)"


class PredictionModel(models.Model):
    """نموذج التنبؤات"""

    name = models.CharField(max_length=100)
    description = models.TextField()
    model_type = models.CharField(max_length=50)
    parameters = models.JSONField()
    accuracy = models.FloatField()
    last_training_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
