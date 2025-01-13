from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from medical_records.models import MedicalRecord

from accounts.models import Clinic, Doctor, Hospital, Patient


class InsuranceCompany(models.Model):
    """شركات التأمين"""

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    contract_start_date = models.DateField()
    contract_end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Insurance Companies"


class InsurancePlan(models.Model):
    """خطط التأمين"""

    PLAN_TYPES = [
        ("basic", "أساسية"),
        ("silver", "فضية"),
        ("gold", "ذهبية"),
        ("platinum", "بلاتينية"),
    ]

    company = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    description = models.TextField()
    annual_limit = models.DecimalField(max_digits=12, decimal_places=2)
    deductible = models.DecimalField(max_digits=10, decimal_places=2)
    copayment_percentage = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company.name} - {self.name}"


class Coverage(models.Model):
    """التغطيات التأمينية"""

    COVERAGE_TYPES = [
        ("consultation", "استشارة طبية"),
        ("medication", "أدوية"),
        ("lab_test", "تحاليل مخبرية"),
        ("radiology", "أشعة"),
        ("surgery", "عملية جراحية"),
        ("hospitalization", "إقامة بالمستشفى"),
        ("dental", "علاج أسنان"),
        ("optical", "نظارات وعدسات"),
        ("maternity", "حمل وولادة"),
        ("chronic", "أمراض مزمنة"),
    ]

    plan = models.ForeignKey(InsurancePlan, on_delete=models.CASCADE)
    coverage_type = models.CharField(max_length=20, choices=COVERAGE_TYPES)
    coverage_limit = models.DecimalField(max_digits=10, decimal_places=2)
    coverage_percentage = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    waiting_period = models.IntegerField(help_text="فترة الانتظار بالأيام")
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.plan.name} - {self.get_coverage_type_display()}"


class InsurancePolicy(models.Model):
    """بوليصة التأمين"""

    STATUS_CHOICES = [
        ("active", "نشطة"),
        ("expired", "منتهية"),
        ("cancelled", "ملغية"),
        ("suspended", "موقوفة"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    plan = models.ForeignKey(InsurancePlan, on_delete=models.CASCADE)
    policy_number = models.CharField(max_length=100, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_limit = models.DecimalField(max_digits=12, decimal_places=2)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.policy_number} - {self.patient.user.get_full_name()}"

    class Meta:
        verbose_name_plural = "Insurance Policies"


class Claim(models.Model):
    """المطالبات التأمينية"""

    STATUS_CHOICES = [
        ("submitted", "مقدمة"),
        ("under_review", "قيد المراجعة"),
        ("approved", "موافق عليها"),
        ("partially_approved", "موافق عليها جزئياً"),
        ("rejected", "مرفوضة"),
        ("paid", "مدفوعة"),
    ]

    policy = models.ForeignKey(InsurancePolicy, on_delete=models.CASCADE)
    claim_number = models.CharField(max_length=100, unique=True)
    service_date = models.DateField()
    service_provider = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    diagnosis = models.TextField()
    service_type = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    covered_amount = models.DecimalField(max_digits=10, decimal_places=2)
    patient_responsibility = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="submitted"
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.claim_number} - {self.policy.patient.user.get_full_name()}"


class ClaimDocument(models.Model):
    """مستندات المطالبة"""

    DOCUMENT_TYPES = [
        ("invoice", "فاتورة"),
        ("prescription", "وصفة طبية"),
        ("medical_report", "تقرير طبي"),
        ("lab_result", "نتيجة تحليل"),
        ("other", "أخرى"),
    ]

    claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to="claim_documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.claim.claim_number}"


class PreApproval(models.Model):
    """الموافقات المسبقة"""

    STATUS_CHOICES = [
        ("pending", "قيد الانتظار"),
        ("approved", "موافق عليه"),
        ("rejected", "مرفوض"),
        ("cancelled", "ملغي"),
    ]

    policy = models.ForeignKey(InsurancePolicy, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=100)
    provider = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)
    approved_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    diagnosis = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    valid_until = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"موافقة مسبقة - {self.policy.patient.user.get_full_name()}"
