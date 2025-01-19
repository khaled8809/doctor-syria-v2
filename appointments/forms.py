"""
وحدة نماذج المواعيد
Appointments Forms Module

This module defines the forms for handling appointment-related data.
"""

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Appointment


class AppointmentForm(forms.ModelForm):
    """
    نموذج الموعد
    Appointment Form

    A form for creating and updating appointments.
    """

    class Meta:
        model = Appointment
        fields = [
            "doctor",
            "appointment_date",
            "reason",
            "notes",
            "priority",
        ]
        widgets = {
            "doctor": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "appointment_date": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                }
            ),
            "reason": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                }
            ),
            "priority": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
        }
        labels = {
            "doctor": _("الطبيب"),
            "appointment_date": _("موعد الزيارة"),
            "reason": _("سبب الزيارة"),
            "notes": _("ملاحظات"),
            "priority": _("الأولوية"),
        }
        help_texts = {
            "reason": _("يرجى ذكر سبب الزيارة بشكل مختصر"),
            "notes": _("أي ملاحظات إضافية"),
            "priority": _("اختر مستوى الأولوية المناسب لحالتك"),
        }
