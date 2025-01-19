"""
وحدة عرض المواعيد
Appointments Views Module

This module handles all appointment-related views, including:
- Creating new appointments
- Viewing appointment details
- Managing appointment status
- Handling appointment notifications
"""

from typing import Any, Dict, List, Optional

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Model
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from doctor_syria.doctor.models import Doctor
from notifications.utils import send_notification

from .forms import AppointmentForm
from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentListView(LoginRequiredMixin, ListView):
    """
    عرض قائمة المواعيد
    List all appointments for the current user
    """

    model = Appointment
    template_name = "appointments/list.html"
    context_object_name = "appointments"

    def get_queryset(self) -> List[Appointment]:
        """
        تصفية المواعيد حسب المستخدم
        Filter appointments based on user type
        """
        user = self.request.user
        if hasattr(user, "doctor_profile"):
            return Appointment.objects.filter(doctor=user.doctor_profile)
        return Appointment.objects.filter(patient__user=user)


class AppointmentDetailView(LoginRequiredMixin, DetailView):
    """
    عرض تفاصيل موعد محدد
    Display details of a specific appointment
    """

    model = Appointment
    template_name = "appointments/detail.html"
    context_object_name = "appointment"

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """إضافة معلومات إضافية للعرض | Add additional context"""
        context = super().get_context_data(**kwargs)
        appointment = self.get_object()
        context["can_cancel"] = appointment.can_be_cancelled()
        context["can_reschedule"] = appointment.can_be_rescheduled()
        return context


@login_required
def create_appointment(request: HttpRequest) -> HttpResponse:
    """
    إنشاء موعد جديد
    Create a new appointment

    Args:
        request: طلب HTTP | HTTP request object

    Returns:
        HttpResponse: استجابة HTTP | HTTP response object
    """
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient_profile
            appointment.save()

            # إرسال إشعار للطبيب | Send notification to doctor
            send_notification(
                recipient=appointment.doctor.user,
                message=f"موعد جديد: {appointment.date} {appointment.time}",
            )

            return JsonResponse({"status": "success"})
    else:
        form = AppointmentForm()

    doctors = Doctor.objects.filter(is_active=True)
    return render(
        request, "appointments/create.html", {"form": form, "doctors": doctors}
    )


@login_required
def cancel_appointment(request: HttpRequest, pk: int) -> HttpResponse:
    """
    إلغاء موعد
    Cancel an appointment

    Args:
        request: طلب HTTP | HTTP request object
        pk: معرف الموعد | Appointment ID

    Returns:
        HttpResponse: استجابة HTTP | HTTP response object
    """
    appointment = get_object_or_404(Appointment, pk=pk)

    if not appointment.can_be_cancelled():
        return JsonResponse({"status": "error", "message": "لا يمكن إلغاء هذا الموعد"})

    appointment.status = "cancelled"
    appointment.save()

    # إرسال إشعار | Send notifications
    send_notification(
        recipient=appointment.doctor.user,
        message=f"تم إلغاء الموعد: {appointment.date} {appointment.time}",
    )
    send_notification(
        recipient=appointment.patient.user, message="تم إلغاء موعدك بنجاح"
    )

    return JsonResponse({"status": "success"})


@login_required
def reschedule_appointment(
    request: HttpRequest, pk: int, new_date: str, new_time: str
) -> HttpResponse:
    """
    إعادة جدولة موعد
    Reschedule an appointment

    Args:
        request: طلب HTTP | HTTP request object
        pk: معرف الموعد | Appointment ID
        new_date: التاريخ الجديد | New date
        new_time: الوقت الجديد | New time

    Returns:
        HttpResponse: استجابة HTTP | HTTP response object
    """
    appointment = get_object_or_404(Appointment, pk=pk)

    if not appointment.can_be_rescheduled():
        return JsonResponse(
            {"status": "error", "message": "لا يمكن إعادة جدولة هذا الموعد"}
        )

    appointment.date = new_date
    appointment.time = new_time
    appointment.save()

    # إرسال إشعار | Send notifications
    send_notification(
        recipient=appointment.doctor.user,
        message=f"تم إعادة جدولة الموعد إلى: {new_date} {new_time}",
    )
    send_notification(
        recipient=appointment.patient.user,
        message=f"تم إعادة جدولة موعدك إلى: {new_date} {new_time}",
    )

    return JsonResponse({"status": "success"})


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    واجهة برمجة التطبيقات للمواعيد
    API endpoint for managing appointments
    """

    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        تصفية المواعيد حسب المستخدم
        Filter appointments based on user type
        """
        user = self.request.user
        if hasattr(user, "doctor_profile"):
            return Appointment.objects.filter(doctor=user.doctor_profile)
        return Appointment.objects.filter(patient=user)

    def perform_create(self, serializer):
        """
        إنشاء موعد جديد
        Create a new appointment
        """
        serializer.save(patient=self.request.user.patient_profile)

        # إرسال إشعار للطبيب | Send notification to doctor
        appointment = serializer.instance
        send_notification(
            recipient=appointment.doctor.user,
            message=f"موعد جديد: {appointment.date} {appointment.time}",
        )

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """
        إلغاء موعد
        Cancel an appointment
        """
        appointment = self.get_object()
        if not appointment.can_be_cancelled():
            return Response(
                {"message": "لا يمكن إلغاء هذا الموعد"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        appointment.status = "cancelled"
        appointment.save()

        # إرسال إشعار | Send notifications
        send_notification(
            recipient=appointment.doctor.user,
            message=f"تم إلغاء الموعد: {appointment.date} {appointment.time}",
        )
        send_notification(
            recipient=appointment.patient.user, message="تم إلغاء موعدك بنجاح"
        )

        return Response({"status": "success"})

    @action(detail=True, methods=["post"])
    def reschedule(self, request, pk=None):
        """
        إعادة جدولة موعد
        Reschedule an appointment
        """
        appointment = self.get_object()
        if not appointment.can_be_rescheduled():
            return Response(
                {"message": "لا يمكن إعادة جدولة هذا الموعد"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_date = request.data.get("date")
        new_time = request.data.get("time")
        if not new_date or not new_time:
            return Response(
                {"message": "يجب تحديد التاريخ والوقت الجديد"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        appointment.date = new_date
        appointment.time = new_time
        appointment.save()

        # إرسال إشعار | Send notifications
        send_notification(
            recipient=appointment.doctor.user,
            message=f"تم إعادة جدولة الموعد إلى: {new_date} {new_time}",
        )
        send_notification(
            recipient=appointment.patient.user,
            message=f"تم إعادة جدولة موعدك إلى: {new_date} {new_time}",
        )

        return Response({"status": "success"})
