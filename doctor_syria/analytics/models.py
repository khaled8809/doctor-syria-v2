from consultations.models import Consultation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from medical_records.models import MedicalRecord

from accounts.models import Clinic, Doctor, Hospital, Patient


class HealthMetric(models.Model):
    """مؤشرات صحية"""

    name = models.CharField(max_length=100)
    description = models.TextField()
    unit = models.CharField(max_length=50)
    normal_range_min = models.DecimalField(max_digits=10, decimal_places=2)
    normal_range_max = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MetricRecord(models.Model):
    """سجلات المؤشرات"""

    metric = models.ForeignKey(HealthMetric, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    # Generic Foreign Key للربط مع أي نوع من الكيانات
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.metric.name}: {self.value} {self.metric.unit}"


class Report(models.Model):
    """التقارير"""

    REPORT_TYPES = [
        ("patient", "تقرير المريض"),
        ("doctor", "تقرير الطبيب"),
        ("hospital", "تقرير المستشفى"),
        ("clinic", "تقرير العيادة"),
        ("disease", "تقرير الأمراض"),
        ("consultation", "تقرير الاستشارات"),
    ]

    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    description = models.TextField()
    parameters = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ReportSchedule(models.Model):
    """جدولة التقارير"""

    FREQUENCY_CHOICES = [
        ("daily", "يومي"),
        ("weekly", "أسبوعي"),
        ("monthly", "شهري"),
        ("quarterly", "ربع سنوي"),
        ("yearly", "سنوي"),
    ]

    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    recipients = models.ManyToManyField("accounts.User")
    is_active = models.BooleanField(default=True)
    last_run = models.DateTimeField(null=True, blank=True)
    next_run = models.DateTimeField()

    def __str__(self):
        return f"جدولة {self.report.title}"


class PerformanceMetric(models.Model):
    """مؤشرات الأداء"""

    METRIC_TYPES = [
        ("satisfaction", "رضا المرضى"),
        ("wait_time", "وقت الانتظار"),
        ("consultation_duration", "مدة الاستشارة"),
        ("response_time", "وقت الاستجابة"),
        ("success_rate", "معدل النجاح"),
    ]

    name = models.CharField(max_length=100)
    metric_type = models.CharField(max_length=50, choices=METRIC_TYPES)
    description = models.TextField()
    target_value = models.DecimalField(max_digits=10, decimal_places=2)
    current_value = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)

    # Generic Foreign Key للربط مع الأطباء أو المستشفيات أو العيادات
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    period_start = models.DateField()
    period_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.content_object}"

    @property
    def achievement_percentage(self):
        """حساب نسبة تحقيق الهدف"""
        return (self.current_value / self.target_value) * 100


class DiseaseStatistic(models.Model):
    """إحصائيات الأمراض"""

    disease_name = models.CharField(max_length=200)
    total_cases = models.IntegerField()
    active_cases = models.IntegerField()
    recovered_cases = models.IntegerField()
    mortality_rate = models.DecimalField(max_digits=5, decimal_places=2)
    age_group = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    region = models.CharField(max_length=100)
    period_start = models.DateField()
    period_end = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-total_cases"]

    def __str__(self):
        return f"{self.disease_name} - {self.region}"


class PatientSatisfactionSurvey(models.Model):
    """استبيانات رضا المرضى"""

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    doctor_rating = models.IntegerField(choices=RATING_CHOICES)
    communication_rating = models.IntegerField(choices=RATING_CHOICES)
    wait_time_rating = models.IntegerField(choices=RATING_CHOICES)
    facility_rating = models.IntegerField(choices=RATING_CHOICES)
    overall_satisfaction = models.IntegerField(choices=RATING_CHOICES)
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"تقييم {self.patient.user.get_full_name()} للاستشارة {self.consultation.id}"

    @property
    def average_rating(self):
        """متوسط التقييم"""
        ratings = [
            self.doctor_rating,
            self.communication_rating,
            self.wait_time_rating,
            self.facility_rating,
            self.overall_satisfaction,
        ]
        return sum(ratings) / len(ratings)
