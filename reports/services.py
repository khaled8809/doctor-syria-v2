"""
خدمات نظام التقارير والإحصائيات
"""

from datetime import datetime, timedelta

import pandas as pd
from django.db.models import Avg, Count, Max, Min
from django.utils import timezone

from .models import HealthMetric, MedicalReport, StatisticalReport, TreatmentProgress


class ReportingService:
    """خدمة إدارة التقارير والإحصائيات"""

    @staticmethod
    def generate_patient_progress_report(patient, start_date=None, end_date=None):
        """توليد تقرير تقدم المريض"""
        if not start_date:
            start_date = timezone.now() - timedelta(days=30)
        if not end_date:
            end_date = timezone.now()

        # جمع البيانات
        metrics = HealthMetric.objects.filter(
            patient=patient, measured_at__range=(start_date, end_date)
        )
        progress_updates = TreatmentProgress.objects.filter(
            patient=patient, date__range=(start_date, end_date)
        )
        reports = MedicalReport.objects.filter(
            patient=patient, created_at__range=(start_date, end_date)
        )

        # تحليل البيانات
        metrics_data = {}
        for metric_type, _ in HealthMetric._meta.get_field("metric_type").choices:
            type_metrics = metrics.filter(metric_type=metric_type)
            if type_metrics.exists():
                metrics_data[metric_type] = {
                    "current": type_metrics.latest("measured_at").value,
                    "min": type_metrics.aggregate(Min("value"))["value__min"],
                    "max": type_metrics.aggregate(Max("value"))["value__max"],
                    "avg": type_metrics.aggregate(Avg("value"))["value__avg"],
                }

        # تحليل التقدم
        progress_trend = (
            progress_updates.values("status")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        return {
            "patient_info": {
                "name": patient.full_name,
                "id": patient.id,
            },
            "period": {
                "start": start_date,
                "end": end_date,
            },
            "metrics": metrics_data,
            "progress": {
                "trend": list(progress_trend),
                "latest_status": (
                    progress_updates.latest("date").status
                    if progress_updates.exists()
                    else None
                ),
            },
            "reports_summary": {
                "total": reports.count(),
                "types": reports.values("report_type").annotate(count=Count("id")),
            },
        }

    @staticmethod
    def generate_clinic_statistics(start_date=None, end_date=None):
        """توليد إحصائيات العيادة"""
        if not start_date:
            start_date = timezone.now() - timedelta(days=30)
        if not end_date:
            end_date = timezone.now()

        appointments = Appointment.objects.filter(date__range=(start_date, end_date))
        reports = MedicalReport.objects.filter(created_at__range=(start_date, end_date))

        return {
            "period": {
                "start": start_date,
                "end": end_date,
            },
            "appointments": {
                "total": appointments.count(),
                "status_distribution": dict(
                    appointments.values_list("status").annotate(count=Count("id"))
                ),
                "daily_average": appointments.count()
                / ((end_date - start_date).days or 1),
            },
            "reports": {
                "total": reports.count(),
                "type_distribution": dict(
                    reports.values_list("report_type").annotate(count=Count("id"))
                ),
            },
            "patients": {
                "unique": appointments.values("patient").distinct().count(),
                "new": appointments.filter(
                    patient__created_at__range=(start_date, end_date)
                )
                .values("patient")
                .distinct()
                .count(),
            },
        }

    @staticmethod
    def analyze_treatment_effectiveness(diagnosis, start_date=None, end_date=None):
        """تحليل فعالية العلاج"""
        if not start_date:
            start_date = timezone.now() - timedelta(days=180)
        if not end_date:
            end_date = timezone.now()

        reports = MedicalReport.objects.filter(
            diagnosis__icontains=diagnosis, created_at__range=(start_date, end_date)
        )

        progress_data = (
            TreatmentProgress.objects.filter(report__in=reports)
            .values("status")
            .annotate(count=Count("id"))
        )

        treatment_plans = reports.values_list("treatment_plan", flat=True)
        medications = reports.values_list("medications", flat=True)

        return {
            "diagnosis": diagnosis,
            "period": {
                "start": start_date,
                "end": end_date,
            },
            "total_cases": reports.count(),
            "progress_distribution": list(progress_data),
            "common_treatments": pd.Series(" ".join(treatment_plans).split())
            .value_counts()
            .head(10)
            .to_dict(),
            "common_medications": pd.Series(" ".join(medications).split())
            .value_counts()
            .head(10)
            .to_dict(),
        }

    @staticmethod
    def generate_health_trends(metric_type, period="monthly"):
        """توليد اتجاهات المؤشرات الصحية"""
        if period == "monthly":
            start_date = timezone.now() - timedelta(days=30)
        elif period == "quarterly":
            start_date = timezone.now() - timedelta(days=90)
        elif period == "yearly":
            start_date = timezone.now() - timedelta(days=365)
        else:
            start_date = timezone.now() - timedelta(days=30)

        metrics = HealthMetric.objects.filter(
            metric_type=metric_type, measured_at__gte=start_date
        )

        df = pd.DataFrame(metrics.values("measured_at", "value", "patient"))
        if not df.empty:
            df["measured_at"] = pd.to_datetime(df["measured_at"])
            df.set_index("measured_at", inplace=True)

            return {
                "metric_type": metric_type,
                "period": period,
                "trends": {
                    "daily_avg": df.resample("D")["value"].mean().to_dict(),
                    "weekly_avg": df.resample("W")["value"].mean().to_dict(),
                    "monthly_avg": df.resample("M")["value"].mean().to_dict(),
                },
                "statistics": {
                    "total_measurements": len(df),
                    "unique_patients": df["patient"].nunique(),
                    "overall_avg": float(df["value"].mean()),
                    "overall_std": float(df["value"].std()),
                },
            }
        return None
