"""
نماذج نظام التقارير والإحصائيات
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from patients.models import Patient

from appointments.models import Appointment


class MedicalReport(models.Model):
    """نموذج التقرير الطبي"""

    REPORT_TYPES = (
        ("initial", "تقرير أولي"),
        ("progress", "تقرير متابعة"),
        ("final", "تقرير نهائي"),
        ("lab", "تقرير مخبري"),
        ("radiology", "تقرير أشعة"),
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="medical_reports",
        verbose_name=_("المريض"),
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_reports",
        verbose_name=_("الطبيب"),
    )
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports",
        verbose_name=_("الموعد"),
    )
    report_type = models.CharField(
        max_length=20, choices=REPORT_TYPES, verbose_name=_("نوع التقرير")
    )
    title = models.CharField(max_length=255, verbose_name=_("عنوان التقرير"))
    content = models.TextField(verbose_name=_("محتوى التقرير"))
    diagnosis = models.TextField(verbose_name=_("التشخيص"))
    treatment_plan = models.TextField(verbose_name=_("خطة العلاج"))
    medications = models.TextField(blank=True, verbose_name=_("الأدوية"))
    attachments = models.JSONField(default=list, blank=True, verbose_name=_("المرفقات"))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("تاريخ الإنشاء")
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("تاريخ التحديث"))

    class Meta:
        verbose_name = _("تقرير طبي")
        verbose_name_plural = _("تقارير طبية")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["patient", "-created_at"]),
            models.Index(fields=["doctor", "-created_at"]),
            models.Index(fields=["report_type", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.get_report_type_display()} - {self.patient.full_name}"


class TreatmentProgress(models.Model):
    """نموذج تتبع تقدم العلاج"""

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="treatment_progress",
        verbose_name=_("المريض"),
    )
    report = models.ForeignKey(
        MedicalReport,
        on_delete=models.CASCADE,
        related_name="progress_updates",
        verbose_name=_("التقرير المرتبط"),
    )
    date = models.DateField(verbose_name=_("تاريخ التحديث"))
    status = models.CharField(
        max_length=50,
        choices=[
            ("improving", "تحسن"),
            ("stable", "مستقر"),
            ("deteriorating", "تدهور"),
            ("recovered", "تعافي"),
        ],
        verbose_name=_("الحالة"),
    )
    notes = models.TextField(verbose_name=_("ملاحظات"))
    metrics = models.JSONField(default=dict, verbose_name=_("مقاييس التقدم"))
    next_steps = models.TextField(blank=True, verbose_name=_("الخطوات التالية"))

    class Meta:
        verbose_name = _("تقدم العلاج")
        verbose_name_plural = _("تقدم العلاج")
        ordering = ["-date"]

    def __str__(self):
        return f"تقدم العلاج - {self.patient.full_name} - {self.date}"


class HealthMetric(models.Model):
    """نموذج المقاييس الصحية"""

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="health_metrics",
        verbose_name=_("المريض"),
    )
    metric_type = models.CharField(
        max_length=50,
        choices=[
            ("blood_pressure", "ضغط الدم"),
            ("heart_rate", "معدل ضربات القلب"),
            ("temperature", "درجة الحرارة"),
            ("weight", "الوزن"),
            ("blood_sugar", "سكر الدم"),
            ("oxygen_level", "مستوى الأكسجين"),
        ],
        verbose_name=_("نوع القياس"),
    )
    value = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name=_("القيمة")
    )
    unit = models.CharField(max_length=20, verbose_name=_("الوحدة"))
    measured_at = models.DateTimeField(verbose_name=_("وقت القياس"))
    notes = models.TextField(blank=True, verbose_name=_("ملاحظات"))
    is_abnormal = models.BooleanField(default=False, verbose_name=_("قيمة غير طبيعية"))
    reference_range = models.CharField(
        max_length=50, blank=True, verbose_name=_("النطاق المرجعي")
    )

    class Meta:
        verbose_name = _("قياس صحي")
        verbose_name_plural = _("قياسات صحية")
        ordering = ["-measured_at"]
        indexes = [
            models.Index(fields=["patient", "metric_type", "-measured_at"]),
        ]

    def __str__(self):
        return f"{self.get_metric_type_display()} - {self.patient.full_name}"


class StatisticalReport(models.Model):
    """نموذج التقارير الإحصائية"""

    REPORT_PERIODS = (
        ("daily", "يومي"),
        ("weekly", "أسبوعي"),
        ("monthly", "شهري"),
        ("quarterly", "ربع سنوي"),
        ("yearly", "سنوي"),
    )

    title = models.CharField(max_length=255, verbose_name=_("عنوان التقرير"))
    period = models.CharField(
        max_length=20, choices=REPORT_PERIODS, verbose_name=_("الفترة")
    )
    start_date = models.DateField(verbose_name=_("تاريخ البداية"))
    end_date = models.DateField(verbose_name=_("تاريخ النهاية"))
    data = models.JSONField(verbose_name=_("البيانات الإحصائية"))
    summary = models.TextField(verbose_name=_("ملخص التقرير"))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="generated_reports",
        verbose_name=_("منشئ التقرير"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("تاريخ الإنشاء")
    )
    is_public = models.BooleanField(default=False, verbose_name=_("عام"))
    categories = models.JSONField(default=list, verbose_name=_("التصنيفات"))
    visualization_settings = models.JSONField(
        default=dict, verbose_name=_("إعدادات العرض المرئي")
    )

    class Meta:
        verbose_name = _("تقرير إحصائي")
        verbose_name_plural = _("تقارير إحصائية")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.get_period_display()}"
