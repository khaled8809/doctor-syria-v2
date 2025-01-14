from rest_framework import serializers

from .models import (
    AIModel,
    DiagnosisResult,
    DiagnosisSession,
    Disease,
    PredictionModel,
    SessionSymptom,
    Symptom,
)


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = ["id", "name", "description", "severity_level", "keywords"]


class DiseaseSerializer(serializers.ModelSerializer):
    symptoms = SymptomSerializer(many=True, read_only=True)

    class Meta:
        model = Disease
        fields = [
            "id",
            "name",
            "description",
            "symptoms",
            "icd_code",
            "risk_level",
            "common_treatments",
        ]


class SessionSymptomSerializer(serializers.ModelSerializer):
    symptom = SymptomSerializer(read_only=True)

    class Meta:
        model = SessionSymptom
        fields = ["symptom", "severity", "notes", "recorded_at"]


class DiagnosisSessionSerializer(serializers.ModelSerializer):
    symptoms = SessionSymptomSerializer(
        source="sessionsymptom_set", many=True, read_only=True
    )

    class Meta:
        model = DiagnosisSession
        fields = [
            "id",
            "patient",
            "doctor",
            "ai_model",
            "symptoms",
            "status",
            "start_time",
            "end_time",
            "notes",
        ]
        read_only_fields = ["start_time", "end_time"]


class DiagnosisResultSerializer(serializers.ModelSerializer):
    disease = DiseaseSerializer(read_only=True)

    class Meta:
        model = DiagnosisResult
        fields = [
            "id",
            "session",
            "disease",
            "confidence",
            "reasoning",
            "recommendations",
            "created_at",
        ]
        read_only_fields = ["created_at"]


class AIModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIModel
        fields = [
            "id",
            "name",
            "model_type",
            "version",
            "description",
            "accuracy",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class PredictionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionModel
        fields = [
            "id",
            "name",
            "description",
            "model_type",
            "parameters",
            "accuracy",
            "last_training_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class SymptomInputSerializer(serializers.Serializer):
    symptom_id = serializers.IntegerField()
    severity = serializers.IntegerField(min_value=1, max_value=3)
    notes = serializers.CharField(required=False, allow_blank=True)


class DiagnosisInputSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField()
    symptoms = SymptomInputSerializer(many=True)
    notes = serializers.CharField(required=False, allow_blank=True)


class PredictionInputSerializer(serializers.Serializer):
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    parameters = serializers.JSONField(required=False)

    def validate(self, data):
        if data["start_date"] >= data["end_date"]:
            raise serializers.ValidationError(
                "تاريخ البداية يجب أن يكون قبل تاريخ النهاية"
            )
        return data
