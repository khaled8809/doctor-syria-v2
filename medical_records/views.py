"""
Views for the medical records app
"""

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from core.cache_decorators import cache_response
from core.cache_manager import CacheManager
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import MedicalRecord
from .forms import MedicalRecordForm

# سيتم إضافة المزيد من الـ views لاحقاً

class RecordListView(LoginRequiredMixin, ListView):
    model = MedicalRecord
    template_name = 'medical_records/record_list.html'
    context_object_name = 'records'
    paginate_by = 10

    def get_queryset(self):
        """تخصيص نتائج البحث حسب المستخدم"""
        if self.request.user.is_staff:
            return MedicalRecord.objects.all()
        return MedicalRecord.objects.filter(patient=self.request.user)

class RecordCreateView(LoginRequiredMixin, CreateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'medical_records/record_form.html'
    success_url = reverse_lazy('medical_records:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class RecordDetailView(LoginRequiredMixin, DetailView):
    model = MedicalRecord
    template_name = 'medical_records/record_detail.html'
    context_object_name = 'record'

class RecordUpdateView(LoginRequiredMixin, UpdateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'medical_records/record_form.html'
    success_url = reverse_lazy('medical_records:list')

class RecordDeleteView(LoginRequiredMixin, DeleteView):
    model = MedicalRecord
    template_name = 'medical_records/record_confirm_delete.html'
    success_url = reverse_lazy('medical_records:list')

# الـ ViewSets الحالية تبقى كما هي
class PatientViewSet(viewsets.ModelViewSet):
    # ... الإعدادات الحالية ...

    @cache_response(timeout=1800, key_prefix='patient_profile')
    def retrieve(self, request, *args, **kwargs):
        """عرض معلومات المريض مع التخزين المؤقت"""
        return super().retrieve(request, *args, **kwargs)

    @cache_response(timeout=3600, key_prefix='patient_medical_history')
    @action(detail=True, methods=['get'])
    def medical_history(self, request, pk=None):
        """عرض التاريخ الطبي للمريض مع التخزين المؤقت"""
        patient = self.get_object()
        history = patient.get_medical_history()
        serializer = MedicalHistorySerializer(history, many=True)
        return Response(serializer.data)

    @cache_response(timeout=900, key_prefix='patient_appointments')  # 15 دقيقة
    @action(detail=True, methods=['get'])
    def upcoming_appointments(self, request, pk=None):
        """عرض المواعيد القادمة للمريض مع التخزين المؤقت"""
        patient = self.get_object()
        appointments = patient.get_upcoming_appointments()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
