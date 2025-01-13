"""
واجهة برمجة التطبيقات للتقارير والإحصائيات
"""

from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import HealthMetric, MedicalReport, StatisticalReport, TreatmentProgress
from .services import ReportingService


class MedicalReportViewSet(viewsets.ModelViewSet):
    """واجهة التقارير الطبية"""

    queryset = MedicalReport.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """تخصيص الاستعلام"""
        queryset = super().get_queryset()

        # تصفية حسب المريض
        patient_id = self.request.query_params.get("patient_id")
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)

        # تصفية حسب نوع التقرير
        report_type = self.request.query_params.get("report_type")
        if report_type:
            queryset = queryset.filter(report_type=report_type)

        # تصفية حسب الفترة الزمنية
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        if start_date and end_date:
            queryset = queryset.filter(created_at__range=(start_date, end_date))

        return queryset

    @action(detail=True, methods=["post"])
    def add_progress_update(self, request, pk=None):
        """إضافة تحديث تقدم للتقرير"""
        report = self.get_object()

        try:
            progress = TreatmentProgress.objects.create(
                patient=report.patient,
                report=report,
                date=timezone.now().date(),
                status=request.data.get("status"),
                notes=request.data.get("notes", ""),
                metrics=request.data.get("metrics", {}),
                next_steps=request.data.get("next_steps", ""),
            )
            return Response(
                {"message": "تم إضافة تحديث التقدم بنجاح", "progress_id": progress.id}
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class HealthMetricViewSet(viewsets.ModelViewSet):
    """واجهة القياسات الصحية"""

    queryset = HealthMetric.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """تخصيص الاستعلام"""
        queryset = super().get_queryset()

        patient_id = self.request.query_params.get("patient_id")
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)

        metric_type = self.request.query_params.get("metric_type")
        if metric_type:
            queryset = queryset.filter(metric_type=metric_type)

        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        if start_date and end_date:
            queryset = queryset.filter(measured_at__range=(start_date, end_date))

        return queryset

    @action(detail=False, methods=["get"])
    def trends(self, request):
        """الحصول على اتجاهات المؤشرات الصحية"""
        metric_type = request.query_params.get("metric_type")
        period = request.query_params.get("period", "monthly")

        if not metric_type:
            return Response(
                {"error": "يجب تحديد نوع المؤشر"}, status=status.HTTP_400_BAD_REQUEST
            )

        trends = ReportingService.generate_health_trends(metric_type, period)
        return Response(trends)


class StatisticalReportViewSet(viewsets.ModelViewSet):
    """واجهة التقارير الإحصائية"""

    queryset = StatisticalReport.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"])
    def clinic_statistics(self, request):
        """الحصول على إحصائيات العيادة"""
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        statistics = ReportingService.generate_clinic_statistics(start_date, end_date)
        return Response(statistics)

    @action(detail=False, methods=["get"])
    def treatment_effectiveness(self, request):
        """تحليل فعالية العلاج"""
        diagnosis = request.query_params.get("diagnosis")
        if not diagnosis:
            return Response(
                {"error": "يجب تحديد التشخيص"}, status=status.HTTP_400_BAD_REQUEST
            )

        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        analysis = ReportingService.analyze_treatment_effectiveness(
            diagnosis, start_date, end_date
        )
        return Response(analysis)

    @action(detail=False, methods=["get"])
    def patient_progress(self, request):
        """تقرير تقدم المريض"""
        patient_id = request.query_params.get("patient_id")
        if not patient_id:
            return Response(
                {"error": "يجب تحديد المريض"}, status=status.HTTP_400_BAD_REQUEST
            )

        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        progress_report = ReportingService.generate_patient_progress_report(
            patient_id, start_date, end_date
        )
        return Response(progress_report)
