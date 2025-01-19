"""
Views for the appointments application.
"""
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response

from accounts.models import Doctor, Patient
from notifications.utils import send_notification

from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing appointments.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Create a new appointment and send notifications.
        """
        appointment = serializer.save()
        
        # Send notification to doctor
        send_notification(
            user=appointment.doctor.user,
            title="موعد جديد",
            message=f"لديك موعد جديد مع {appointment.patient.user.get_full_name()} في {appointment.date}",
            notification_type="info",
            related_object=appointment
        )
        
        # Send notification to patient
        send_notification(
            user=appointment.patient.user,
            title="تأكيد الموعد",
            message=f"تم تأكيد موعدك مع د. {appointment.doctor.user.get_full_name()} في {appointment.date}",
            notification_type="success",
            related_object=appointment
        )

    def perform_update(self, serializer):
        """
        Update an appointment and send notifications.
        """
        appointment = serializer.save()
        
        if appointment.status == "confirmed":
            send_notification(
                user=appointment.patient.user,
                title="تأكيد الموعد",
                message=f"تم تأكيد موعدك مع د. {appointment.doctor.user.get_full_name()}",
                notification_type="success",
                related_object=appointment
            )
        elif appointment.status == "cancelled":
            send_notification(
                user=appointment.patient.user,
                title="إلغاء الموعد",
                message=f"تم إلغاء موعدك مع د. {appointment.doctor.user.get_full_name()}",
                notification_type="warning",
                related_object=appointment
            )

    def get_queryset(self):
        """
        Filter appointments based on user role.
        """
        user = self.request.user
        if hasattr(user, 'doctor'):
            return Appointment.objects.filter(doctor=user.doctor)
        elif hasattr(user, 'patient'):
            return Appointment.objects.filter(patient=user.patient)
        return Appointment.objects.none()
