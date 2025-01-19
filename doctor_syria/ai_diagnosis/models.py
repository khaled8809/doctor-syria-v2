from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class AIAnalysis(models.Model):
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="ai_analyses"
    )
    analysis_type = models.CharField(max_length=100)
    input_data = models.JSONField()
    results = models.JSONField()
    confidence_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} - {self.analysis_type}"


class ImageAnalysis(models.Model):
    image = models.ImageField(upload_to="ai_analysis/images/")
    analysis_type = models.CharField(max_length=100)
    results = models.JSONField()
    confidence_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.analysis_type} - {self.created_at}"


class DrugInteraction(models.Model):
    drug_combination = models.JSONField()  # List of drugs being checked
    interaction_level = models.CharField(max_length=50)  # Severe, Moderate, Mild
    description = models.TextField()
    recommendations = models.TextField()

    def __str__(self):
        return f"Interaction: {self.interaction_level}"
