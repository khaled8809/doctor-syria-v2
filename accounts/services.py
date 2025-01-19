"""
خدمات تطبيق الحسابات
"""

from django.utils import timezone

from appointments.models import Appointment
from notifications.models import Notification
from pharmacy.models import Prescription


def get_upcoming_appointments(user):
    """الحصول على المواعيد القادمة"""
    return Appointment.objects.filter(
        patient=user.patient_profile,
        appointment_date__gte=timezone.now(),
    ).order_by("appointment_date")[:5]


def get_new_prescriptions_count(user):
    """الحصول على عدد الوصفات الطبية الجديدة"""
    return Prescription.objects.filter(
        patient=user.patient_profile,
        created_at__gte=timezone.now() - timezone.timedelta(days=7),
    ).count()


def get_user_notifications(user):
    """الحصول على إشعارات المستخدم"""
    return Notification.objects.filter(
        user=user,
        is_read=False,
    ).order_by("-created_at")[:5]
