"""
Views for the medical records app
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.cache_decorators import cache_response
from core.cache_manager import CacheManager

from .forms import MedicalRecordForm, MedicalVisitForm
from .models import MedicalRecord, MedicalVisit

# سيتم إضافة المزيد من الـ views لاحقاً


class RecordListView(LoginRequiredMixin, ListView):
    model = MedicalRecord
    template_name = "medical_records/record_list.html"
    context_object_name = "records"
    paginate_by = 10

    def get_queryset(self):
        """تخصيص نتائج البحث حسب المستخدم"""
        if self.request.user.is_staff:
            return MedicalRecord.objects.all()
        return MedicalRecord.objects.filter(patient=self.request.user)


class RecordCreateView(LoginRequiredMixin, CreateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = "medical_records/record_form.html"
    success_url = reverse_lazy("medical_records:list")

    def form_valid(self, form):
        form.instance.patient = self.request.user
        return super().form_valid(form)


class RecordDetailView(LoginRequiredMixin, DetailView):
    model = MedicalRecord
    template_name = "medical_records/record_detail.html"
    context_object_name = "record"


class RecordUpdateView(LoginRequiredMixin, UpdateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = "medical_records/record_form.html"
    success_url = reverse_lazy("medical_records:list")


class RecordDeleteView(LoginRequiredMixin, DeleteView):
    model = MedicalRecord
    template_name = "medical_records/record_confirm_delete.html"
    success_url = reverse_lazy("medical_records:list")


# الـ ViewSets الحالية تبقى كما هي
class PatientViewSet(viewsets.ModelViewSet):
    """ViewSet للمرضى"""

    @cache_response(timeout=300)
    def retrieve(self, request, *args, **kwargs):
        """عرض معلومات المريض مع التخزين المؤقت"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    @cache_response(timeout=300)
    def medical_history(self, request, pk=None):
        """عرض التاريخ الطبي للمريض مع التخزين المؤقت"""
        patient = self.get_object()
        visits = MedicalVisit.objects.filter(patient=patient).order_by("-visit_date")
        serializer = MedicalVisitSerializer(visits, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    @cache_response(timeout=300)
    def upcoming_appointments(self, request, pk=None):
        """عرض المواعيد القادمة للمريض مع التخزين المؤقت"""
        patient = self.get_object()
        upcoming = MedicalVisit.objects.filter(
            patient=patient, visit_date__gt=timezone.now()
        ).order_by("visit_date")
        serializer = MedicalVisitSerializer(upcoming, many=True)
        return Response(serializer.data)
