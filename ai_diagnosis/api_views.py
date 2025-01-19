from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    AIModel,
    DiagnosisResult,
    DiagnosisSession,
    Disease,
    PredictionModel,
    Symptom,
)
from .serializers import (
    DiagnosisResultSerializer,
    DiagnosisSessionSerializer,
    DiseaseSerializer,
    SymptomSerializer,
)
from .services import DiagnosisService, PredictionService


class DiagnosisViewSet(viewsets.ModelViewSet):
    """واجهة برمجة التشخيص الذكي"""

    queryset = DiagnosisSession.objects.all()
    serializer_class = DiagnosisSessionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def start_diagnosis(self, request, pk=None):
        """بدء جلسة تشخيص جديدة"""
        session = self.get_object()

        # التحقق من الصلاحيات
        if session.doctor != request.user:
            return Response(
                {"error": "غير مصرح لك بإجراء هذا التشخيص"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # التحقق من الحالة
        if session.status != "ACTIVE":
            return Response(
                {"error": "لا يمكن بدء التشخيص - الجلسة غير نشطة"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # إنشاء خدمة التشخيص
            diagnosis_service = DiagnosisService(session)

            # تحليل الأعراض
            results = diagnosis_service.analyze_symptoms()

            return Response({"session_id": session.id, "results": results})
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=["post"])
    def add_symptom(self, request, pk=None):
        """إضافة عرض للجلسة"""
        session = self.get_object()
        symptom_id = request.data.get("symptom_id")
        severity = request.data.get("severity")

        if not all([symptom_id, severity]):
            return Response(
                {"error": "يجب توفير معرف العرض ودرجة شدته"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            symptom = get_object_or_404(Symptom, id=symptom_id)
            session.symptoms.add(symptom, through_defaults={"severity": severity})
            return Response({"message": "تمت إضافة العرض بنجاح"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def get_results(self, request, pk=None):
        """الحصول على نتائج التشخيص"""
        session = self.get_object()
        results = DiagnosisResult.objects.filter(session=session)
        serializer = DiagnosisResultSerializer(results, many=True)
        return Response(serializer.data)


class PredictionViewSet(viewsets.ViewSet):
    """واجهة برمجة التنبؤات"""

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def predict_patient_risks(self, request):
        """التنبؤ بالمخاطر الصحية للمريض"""
        patient_data = request.data.get("patient_data")
        if not patient_data:
            return Response(
                {"error": "يجب توفير بيانات المريض"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            prediction_service = PredictionService()
            results = prediction_service.predict_patient_risks(patient_data)
            return Response(results)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["post"])
    def predict_appointment_load(self, request):
        """التنبؤ بحجم المواعيد"""
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")

        if not all([start_date, end_date]):
            return Response(
                {"error": "يجب توفير نطاق التاريخ"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            prediction_service = PredictionService()
            results = prediction_service.predict_appointment_load(
                (start_date, end_date)
            )
            return Response(results)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["post"])
    def predict_resource_needs(self, request):
        """التنبؤ باحتياجات الموارد"""
        timeframe = request.data.get("timeframe")
        if not timeframe:
            return Response(
                {"error": "يجب توفير الإطار الزمني"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            prediction_service = PredictionService()
            results = prediction_service.predict_resource_needs(timeframe)
            return Response(results)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
