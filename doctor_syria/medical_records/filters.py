import django_filters
from django.utils.translation import gettext_lazy as _

from .models import Allergy, Appointment, MedicalRecord, Prescription, Vaccination


class MedicalRecordFilter(django_filters.FilterSet):
    """
    فلتر السجلات الطبية
    """

    date_from = django_filters.DateTimeFilter(
        field_name="date", lookup_expr="gte", label=_("من تاريخ")
    )
    date_to = django_filters.DateTimeFilter(
        field_name="date", lookup_expr="lte", label=_("إلى تاريخ")
    )

    class Meta:
        model = MedicalRecord
        fields = {
            "record_type": ["exact"],
            "severity": ["exact"],
            "doctor": ["exact"],
            "patient": ["exact"],
        }


class AppointmentFilter(django_filters.FilterSet):
    """
    فلتر المواعيد
    """

    scheduled_from = django_filters.DateTimeFilter(
        field_name="scheduled_time", lookup_expr="gte", label=_("من تاريخ")
    )
    scheduled_to = django_filters.DateTimeFilter(
        field_name="scheduled_time", lookup_expr="lte", label=_("إلى تاريخ")
    )

    class Meta:
        model = Appointment
        fields = {
            "status": ["exact"],
            "appointment_type": ["exact"],
            "doctor": ["exact"],
            "patient": ["exact"],
        }


class PrescriptionFilter(django_filters.FilterSet):
    """
    فلتر الوصفات الطبية
    """

    created_from = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte", label=_("من تاريخ")
    )
    created_to = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte", label=_("إلى تاريخ")
    )

    class Meta:
        model = Prescription
        fields = {
            "is_chronic": ["exact"],
            "medical_record": ["exact"],
            "medical_record__doctor": ["exact"],
            "medical_record__patient": ["exact"],
        }


class AllergyFilter(django_filters.FilterSet):
    """
    فلتر الحساسية
    """

    diagnosis_from = django_filters.DateFilter(
        field_name="diagnosis_date", lookup_expr="gte", label=_("من تاريخ")
    )
    diagnosis_to = django_filters.DateFilter(
        field_name="diagnosis_date", lookup_expr="lte", label=_("إلى تاريخ")
    )

    class Meta:
        model = Allergy
        fields = {
            "allergy_type": ["exact"],
            "reaction": ["exact"],
            "patient": ["exact"],
        }


class VaccinationFilter(django_filters.FilterSet):
    """
    فلتر التطعيمات
    """

    date_from = django_filters.DateFilter(
        field_name="date_given", lookup_expr="gte", label=_("من تاريخ")
    )
    date_to = django_filters.DateFilter(
        field_name="date_given", lookup_expr="lte", label=_("إلى تاريخ")
    )

    class Meta:
        model = Vaccination
        fields = {
            "vaccine_type": ["exact"],
            "patient": ["exact"],
            "given_by": ["exact"],
        }
