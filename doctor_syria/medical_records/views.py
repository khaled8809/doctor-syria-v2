from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import MedicalRecord
from .forms import MedicalRecordForm

from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import (
    MedicalRecord, Appointment, Prescription,
    Allergy, Vaccination
)
from .serializers import (
    MedicalRecordSerializer, AppointmentSerializer,
    PrescriptionSerializer, AllergySerializer,
    VaccinationSerializer
)
from .filters import (
    MedicalRecordFilter, AppointmentFilter,
    PrescriptionFilter, AllergyFilter,
    VaccinationFilter
)

class RecordListView(LoginRequiredMixin, ListView):
    model = MedicalRecord
    template_name = 'medical_records/record_list.html'
    context_object_name = 'records'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return MedicalRecord.objects.filter(doctor=user.doctor)
        elif user.role == 'patient':
            return MedicalRecord.objects.filter(patient=user.patient)
        return MedicalRecord.objects.none()

class RecordDetailView(LoginRequiredMixin, DetailView):
    model = MedicalRecord
    template_name = 'medical_records/record_detail.html'
    context_object_name = 'record'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return MedicalRecord.objects.filter(doctor=user.doctor)
        elif user.role == 'patient':
            return MedicalRecord.objects.filter(patient=user.patient)
        return MedicalRecord.objects.none()

class RecordCreateView(LoginRequiredMixin, CreateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'medical_records/record_form.html'
    success_url = reverse_lazy('medical_records:record_list')

    def form_valid(self, form):
        form.instance.doctor = self.request.user.doctor
        return super().form_valid(form)

class RecordUpdateView(LoginRequiredMixin, UpdateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'medical_records/record_form.html'
    success_url = reverse_lazy('medical_records:record_list')

    def get_queryset(self):
        return MedicalRecord.objects.filter(doctor=self.request.user.doctor)

class RecordDeleteView(LoginRequiredMixin, DeleteView):
    model = MedicalRecord
    template_name = 'medical_records/record_confirm_delete.html'
    success_url = reverse_lazy('medical_records:record_list')

    def get_queryset(self):
        return MedicalRecord.objects.filter(doctor=self.request.user.doctor)

class MedicalRecordViewSet(viewsets.ModelViewSet):
    """
    وجهة نظر السجلات الطبية
    """
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MedicalRecordFilter
    search_fields = ['title', 'description', 'notes']
    ordering_fields = ['date', 'created_at', 'severity']

    def get_queryset(self):
        """
        تخصيص الاستعلام حسب نوع المستخدم
        """
        user = self.request.user
        queryset = super().get_queryset()

        if user.is_doctor:
            return queryset.filter(doctor=user)
        elif user.is_patient:
            return queryset.filter(patient=user)
        
        return queryset

    def perform_create(self, serializer):
        """
        إضافة معلومات المستخدم عند الإنشاء
        """
        serializer.save(
            created_by=self.request.user,
            doctor=self.request.user if self.request.user.is_doctor else None
        )

class AppointmentViewSet(viewsets.ModelViewSet):
    """
    وجهة نظر المواعيد
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AppointmentFilter
    search_fields = ['reason', 'notes']
    ordering_fields = ['scheduled_time', 'created_at', 'status']

    def get_queryset(self):
        """
        تخصيص الاستعلام حسب نوع المستخدم
        """
        user = self.request.user
        queryset = super().get_queryset()

        if user.is_doctor:
            return queryset.filter(doctor=user)
        elif user.is_patient:
            return queryset.filter(patient=user)
        
        return queryset

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        إلغاء الموعد
        """
        appointment = self.get_object()
        reason = request.data.get('reason', '')
        appointment.cancel(reason)
        return Response({'status': 'تم إلغاء الموعد'})

    @action(detail=False)
    def upcoming(self, request):
        """
        المواعيد القادمة
        """
        queryset = self.get_queryset().filter(
            scheduled_time__gte=timezone.now(),
            status='confirmed'
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class PrescriptionViewSet(viewsets.ModelViewSet):
    """
    وجهة نظر الوصفات الطبية
    """
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PrescriptionFilter
    search_fields = ['medicine_name', 'instructions']
    ordering_fields = ['created_at']

    def get_queryset(self):
        """
        تخصيص الاستعلام حسب نوع المستخدم
        """
        user = self.request.user
        queryset = super().get_queryset()

        if user.is_doctor:
            return queryset.filter(medical_record__doctor=user)
        elif user.is_patient:
            return queryset.filter(medical_record__patient=user)
        
        return queryset

class AllergyViewSet(viewsets.ModelViewSet):
    """
    وجهة نظر الحساسية
    """
    queryset = Allergy.objects.all()
    serializer_class = AllergySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AllergyFilter
    search_fields = ['allergen', 'notes']
    ordering_fields = ['diagnosis_date', 'created_at']

    def get_queryset(self):
        """
        تخصيص الاستعلام حسب نوع المستخدم
        """
        user = self.request.user
        queryset = super().get_queryset()

        if user.is_doctor:
            return queryset
        elif user.is_patient:
            return queryset.filter(patient=user)
        
        return queryset

class VaccinationViewSet(viewsets.ModelViewSet):
    """
    وجهة نظر التطعيمات
    """
    queryset = Vaccination.objects.all()
    serializer_class = VaccinationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = VaccinationFilter
    search_fields = ['vaccine_name', 'notes']
    ordering_fields = ['date_given', 'created_at']

    def get_queryset(self):
        """
        تخصيص الاستعلام حسب نوع المستخدم
        """
        user = self.request.user
        queryset = super().get_queryset()

        if user.is_doctor:
            return queryset
        elif user.is_patient:
            return queryset.filter(patient=user)
        
        return queryset

    @action(detail=False)
    def due_vaccinations(self, request):
        """
        التطعيمات المستحقة
        """
        queryset = self.get_queryset().filter(
            next_dose_date__lte=timezone.now()
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
