"""
مهام Celery لتحديث البيانات المخزنة مؤقتاً وتحسين الأداء
"""

from datetime import timedelta

from celery import shared_task
from django.core.cache import cache
from django.db import connection
from django.utils import timezone


@shared_task
def refresh_materialized_views():
    """تحديث الجداول المؤقتة"""
    with connection.cursor() as cursor:
        cursor.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY mv_appointment_stats")
        cursor.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY mv_patient_metrics")


@shared_task
def cleanup_old_sessions():
    """تنظيف الجلسات القديمة"""
    from django.core.management.commands.clearsessions import Command

    Command().handle()


@shared_task
def cache_common_queries():
    """تخزين نتائج الاستعلامات الشائعة مؤقتاً"""
    from core.models import Appointment, Patient
    from reports.models import MedicalReport

    # إحصائيات المرضى
    patient_stats = {
        "total": Patient.objects.count(),
        "active": Patient.objects.filter(is_active=True).count(),
        "new_this_month": Patient.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count(),
    }
    cache.set("patient_stats", patient_stats, timeout=3600)  # ساعة واحدة

    # إحصائيات المواعيد
    today = timezone.now().date()
    appointment_stats = {
        "today": Appointment.objects.filter(appointment_date__date=today).count(),
        "pending": Appointment.objects.filter(status="pending").count(),
        "completed_this_week": Appointment.objects.filter(
            status="completed", appointment_date__gte=today - timedelta(days=7)
        ).count(),
    }
    cache.set("appointment_stats", appointment_stats, timeout=1800)  # 30 دقيقة

    # التقارير الأخيرة
    recent_reports = MedicalReport.objects.select_related("patient", "doctor").order_by(
        "-created_at"
    )[:10]
    cache.set("recent_reports", list(recent_reports), timeout=900)  # 15 دقيقة


@shared_task
def optimize_database():
    """تحسين قاعدة البيانات"""
    with connection.cursor() as cursor:
        # تحليل الجداول
        cursor.execute(
            """
            ANALYZE core_patient;
            ANALYZE core_appointment;
            ANALYZE reports_medicalreport;
            ANALYZE reports_healthmetric;
        """
        )

        # تنظيف وتحسين الجداول
        cursor.execute(
            """
            VACUUM ANALYZE core_patient;
            VACUUM ANALYZE core_appointment;
            VACUUM ANALYZE reports_medicalreport;
            VACUUM ANALYZE reports_healthmetric;
        """
        )


@shared_task
def cleanup_old_notifications():
    """حذف الإشعارات القديمة"""
    from notifications.models import Notification

    # حذف الإشعارات المقروءة الأقدم من شهر
    Notification.objects.filter(
        is_read=True, created_at__lt=timezone.now() - timedelta(days=30)
    ).delete()


@shared_task
def update_search_index():
    """تحديث فهرس البحث"""
    with connection.cursor() as cursor:
        # تحديث فهرس البحث النصي
        cursor.execute(
            """
            REINDEX INDEX idx_patient_search;
            REINDEX INDEX idx_medical_report_diagnosis;
        """
        )


# جدولة المهام
def setup_periodic_tasks(sender, **kwargs):
    """إعداد المهام الدورية"""
    from celery.schedules import crontab

    # تحديث الجداول المؤقتة كل ساعة
    sender.add_periodic_task(crontab(minute=0), refresh_materialized_views.s())

    # تنظيف الجلسات القديمة يومياً
    sender.add_periodic_task(crontab(hour=2, minute=0), cleanup_old_sessions.s())

    # تخزين الاستعلامات الشائعة كل 30 دقيقة
    sender.add_periodic_task(30 * 60, cache_common_queries.s())

    # تحسين قاعدة البيانات أسبوعياً
    sender.add_periodic_task(
        crontab(day_of_week="sun", hour=3, minute=0), optimize_database.s()
    )

    # تنظيف الإشعارات القديمة يومياً
    sender.add_periodic_task(crontab(hour=1, minute=0), cleanup_old_notifications.s())

    # تحديث فهرس البحث يومياً
    sender.add_periodic_task(crontab(hour=4, minute=0), update_search_index.s())
