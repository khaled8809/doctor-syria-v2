from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import Doctor, Laboratory, Patient

# Create your models here.


class TestCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Test Categories"

    def __str__(self):
        return self.name


class LabTest(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        TestCategory, on_delete=models.CASCADE, related_name="tests"
    )
    description = models.TextField()
    preparation_instructions = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=100)  # e.g., "2 hours", "1 day"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TestRequest(models.Model):
    STATUS_CHOICES = (
        ("pending", _("Pending")),
        ("sample_collected", _("Sample Collected")),
        ("processing", _("Processing")),
        ("completed", _("Completed")),
        ("cancelled", _("Cancelled")),
    )

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="test_requests"
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="test_requests",
        null=True,
        blank=True,
    )
    laboratory = models.ForeignKey(
        Laboratory, on_delete=models.CASCADE, related_name="test_requests"
    )
    test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    requested_date = models.DateTimeField(auto_now_add=True)
    appointment_date = models.DateTimeField()
    completion_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.patient} - {self.test} - {self.status}"


class TestResult(models.Model):
    test_request = models.OneToOneField(
        TestRequest, on_delete=models.CASCADE, related_name="result"
    )
    result_date = models.DateTimeField(auto_now_add=True)
    results = models.JSONField()  # Store test results as JSON
    interpretation = models.TextField()
    is_normal = models.BooleanField()
    notes = models.TextField(blank=True)
    attachments = models.FileField(upload_to="test_results/", null=True, blank=True)

    def __str__(self):
        return f"Results for {self.test_request}"


class SampleCollection(models.Model):
    STATUS_CHOICES = (
        ("pending", _("Pending")),
        ("collected", _("Collected")),
        ("rejected", _("Rejected")),
    )

    test_request = models.OneToOneField(
        TestRequest, on_delete=models.CASCADE, related_name="sample"
    )
    collection_date = models.DateTimeField()
    collected_by = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    sample_type = models.CharField(max_length=100)  # e.g., blood, urine
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Sample for {self.test_request}"


class ReferenceRange(models.Model):
    test = models.ForeignKey(
        LabTest, on_delete=models.CASCADE, related_name="reference_ranges"
    )
    parameter = models.CharField(max_length=100)
    min_value = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    max_value = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    unit = models.CharField(max_length=50)
    gender = models.CharField(
        max_length=20, null=True, blank=True
    )  # For gender-specific ranges
    min_age = models.PositiveIntegerField(
        null=True, blank=True
    )  # For age-specific ranges
    max_age = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.test} - {self.parameter}"
