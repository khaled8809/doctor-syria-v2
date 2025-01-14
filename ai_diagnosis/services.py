from typing import Any, Dict, List

import numpy as np
from sklearn.ensemble import RandomForestClassifier

from .models import (
    AIModel,
    DiagnosisResult,
    DiagnosisSession,
    Disease,
    PredictionModel,
    Symptom,
)


class DiagnosisService:
    """خدمة التشخيص الذكي"""

    def __init__(self, session: DiagnosisSession):
        self.session = session
        self.ai_model = session.ai_model

    def analyze_symptoms(self) -> List[Dict[str, Any]]:
        """تحليل الأعراض وتقديم التشخيصات المحتملة"""
        symptoms_data = self._prepare_symptoms_data()
        predictions = self._run_diagnosis_model(symptoms_data)
        return self._format_diagnosis_results(predictions)

    def _prepare_symptoms_data(self) -> np.ndarray:
        """تحضير بيانات الأعراض للتحليل"""
        session_symptoms = self.session.symptoms.all()
        symptoms_vector = []

        for symptom in Symptom.objects.all():
            session_symptom = next(
                (s for s in session_symptoms if s.id == symptom.id), None
            )
            severity = session_symptom.severity if session_symptom else 0
            symptoms_vector.append(severity)

        return np.array(symptoms_vector)

    def _run_diagnosis_model(self, symptoms_data: np.ndarray) -> List[Dict[str, float]]:
        """تشغيل نموذج التشخيص"""
        model = self._load_model()
        predictions = model.predict_proba([symptoms_data])[0]
        diseases = Disease.objects.all()

        return [
            {"disease": disease, "probability": prob}
            for disease, prob in zip(diseases, predictions)
            if prob > 0.1  # تجاهل الاحتمالات المنخفضة
        ]

    def _format_diagnosis_results(
        self, predictions: List[Dict[str, float]]
    ) -> List[Dict[str, Any]]:
        """تنسيق نتائج التشخيص"""
        results = []
        for pred in sorted(predictions, key=lambda x: x["probability"], reverse=True):
            disease = pred["disease"]
            probability = pred["probability"]

            # إنشاء نتيجة التشخيص
            diagnosis_result = DiagnosisResult.objects.create(
                session=self.session,
                disease=disease,
                confidence=probability * 100,
                reasoning=self._generate_reasoning(disease, probability),
                recommendations=self._generate_recommendations(disease),
            )

            results.append(
                {
                    "disease": disease.name,
                    "confidence": probability * 100,
                    "icd_code": disease.icd_code,
                    "reasoning": diagnosis_result.reasoning,
                    "recommendations": diagnosis_result.recommendations,
                }
            )

        return results

    def _generate_reasoning(
        self, disease: Disease, probability: float
    ) -> Dict[str, Any]:
        """توليد تفسير للتشخيص"""
        session_symptoms = self.session.symptoms.all()
        disease_symptoms = disease.symptoms.all()

        matching_symptoms = []
        missing_symptoms = []

        for symptom in disease_symptoms:
            if symptom in session_symptoms:
                matching_symptoms.append(
                    {
                        "name": symptom.name,
                        "importance": symptom.diseasesymptom_set.get(
                            disease=disease
                        ).importance,
                    }
                )
            else:
                missing_symptoms.append(
                    {
                        "name": symptom.name,
                        "importance": symptom.diseasesymptom_set.get(
                            disease=disease
                        ).importance,
                    }
                )

        return {
            "matching_symptoms": matching_symptoms,
            "missing_symptoms": missing_symptoms,
            "confidence_explanation": self._explain_confidence(probability),
        }

    def _generate_recommendations(self, disease: Disease) -> str:
        """توليد التوصيات بناءً على التشخيص"""
        recommendations = [
            "التوصيات الطبية:",
            "==================",
        ]

        if disease.common_treatments:
            recommendations.extend(
                [
                    "العلاجات الشائعة:",
                    *[f"- {treatment}" for treatment in disease.common_treatments],
                ]
            )

        if disease.risk_level >= 2:
            recommendations.append("\nملاحظة: يُنصح بمراجعة الطبيب في أقرب وقت ممكن.")

        return "\n".join(recommendations)

    def _explain_confidence(self, probability: float) -> str:
        """شرح مستوى الثقة في التشخيص"""
        if probability > 0.8:
            return "ثقة عالية بناءً على تطابق الأعراض الرئيسية"
        elif probability > 0.5:
            return "ثقة متوسطة مع وجود بعض الأعراض المطابقة"
        else:
            return "ثقة منخفضة، يُنصح بمزيد من الفحوصات"


class PredictionService:
    """خدمة التنبؤات الطبية"""

    def predict_patient_risks(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """التنبؤ بالمخاطر الصحية للمريض"""
        # تنفيذ منطق التنبؤ
        pass

    def predict_appointment_load(self, date_range: tuple) -> Dict[str, Any]:
        """التنبؤ بحجم المواعيد"""
        # تنفيذ منطق التنبؤ
        pass

    def predict_resource_needs(self, timeframe: str) -> Dict[str, Any]:
        """التنبؤ باحتياجات الموارد"""
        # تنفيذ منطق التنبؤ
        pass
