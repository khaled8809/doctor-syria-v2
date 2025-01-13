from django.conf import settings
from django.db import models

from laboratory.models import TestResult


class ClinicalDecision(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    patient = models.ForeignKey("accounts.Patient", on_delete=models.CASCADE)
    symptoms = models.TextField()
    suggested_diagnosis = models.TextField()
    recommended_tests = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Decision for {self.patient} by {self.doctor}"


class TreatmentProtocol(models.Model):
    name = models.CharField(max_length=200)
    condition = models.CharField(max_length=200)
    description = models.TextField()
    steps = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class LabResultAnalysis(models.Model):
    test_result = models.ForeignKey(TestResult, on_delete=models.CASCADE)
    analysis_date = models.DateTimeField(auto_now_add=True)
    findings = models.TextField()
    recommendations = models.TextField()
    is_critical = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Analysis of {self.test_result} by {self.reviewed_by}"
