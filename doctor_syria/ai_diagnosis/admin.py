from django.contrib import admin

from .models import AIAnalysis, DrugInteraction, ImageAnalysis


@admin.register(AIAnalysis)
class AIAnalysisAdmin(admin.ModelAdmin):
    list_display = ("patient", "analysis_type", "confidence_score", "created_at")
    list_filter = ("analysis_type",)
    search_fields = ("patient__username", "analysis_type")


@admin.register(ImageAnalysis)
class ImageAnalysisAdmin(admin.ModelAdmin):
    list_display = ("analysis_type", "confidence_score", "created_at")
    list_filter = ("analysis_type",)
    search_fields = ("analysis_type",)


@admin.register(DrugInteraction)
class DrugInteractionAdmin(admin.ModelAdmin):
    list_display = ("interaction_level",)
    list_filter = ("interaction_level",)
    search_fields = ("description",)
