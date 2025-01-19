from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class PreventiveCheckup(models.Model):
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="preventive_checkups"
    )
    checkup_type = models.CharField(max_length=100)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} - {self.checkup_type}"


class Vaccination(models.Model):
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="vaccinations"
    )
    vaccine_name = models.CharField(max_length=100)
    due_date = models.DateField()
    administered_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.patient.username} - {self.vaccine_name}"


class HealthTip(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    target_conditions = models.JSONField(
        default=dict
    )  # Store conditions this tip applies to
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
