from datetime import datetime, timedelta
from typing import Dict, List

from django.db.models import Avg, Count
from django.utils import timezone


class AnalyticsService:
    @staticmethod
    def get_hospital_statistics(
        start_date: datetime = None, end_date: datetime = None
    ) -> Dict:
        """إحصائيات المستشفى"""
        if not start_date:
            start_date = timezone.now() - timedelta(days=30)
        if not end_date:
            end_date = timezone.now()

        from medical_records.models import PatientVisit

        from accounts.models import User
        from appointments.models import Appointment

        return {
            "total_patients": User.objects.filter(role="patient").count(),
            "total_doctors": User.objects.filter(role="doctor").count(),
            "appointments": Appointment.objects.filter(
                date__range=(start_date, end_date)
            ).count(),
            "visits": PatientVisit.objects.filter(
                date__range=(start_date, end_date)
            ).count(),
        }

    @staticmethod
    def get_department_performance() -> List[Dict]:
        """أداء الأقسام"""
        from medical_records.models import PatientVisit

        return list(
            PatientVisit.objects.values("department")
            .annotate(total_visits=Count("id"), avg_duration=Avg("duration"))
            .order_by("-total_visits")
        )

    @staticmethod
    def get_ai_diagnosis_accuracy() -> Dict:
        """دقة التشخيص بالذكاء الاصطناعي"""
        from ai_diagnosis.models import AIDiagnosis

        total = AIDiagnosis.objects.count()
        correct = AIDiagnosis.objects.filter(is_correct=True).count()

        return {
            "total_diagnoses": total,
            "correct_diagnoses": correct,
            "accuracy": (correct / total * 100) if total > 0 else 0,
        }

    @staticmethod
    def get_pharmacy_inventory() -> Dict:
        """تحليل مخزون الصيدلية"""
        from pharmacy.models import Medicine

        return {
            "total_medicines": Medicine.objects.count(),
            "low_stock": Medicine.objects.filter(quantity__lte=10).count(),
            "out_of_stock": Medicine.objects.filter(quantity=0).count(),
            "expiring_soon": Medicine.objects.filter(
                expiry_date__lte=timezone.now() + timedelta(days=90)
            ).count(),
        }

    @staticmethod
    def get_financial_summary(year: int = None) -> Dict:
        """ملخص مالي"""
        if not year:
            year = timezone.now().year

        from billing.models import Invoice

        invoices = Invoice.objects.filter(date__year=year)
        return {
            "total_revenue": sum(inv.total for inv in invoices),
            "paid_invoices": invoices.filter(status="paid").count(),
            "pending_invoices": invoices.filter(status="pending").count(),
            "monthly_revenue": list(
                invoices.values("date__month")
                .annotate(total=Sum("total"))
                .order_by("date__month")
            ),
        }
