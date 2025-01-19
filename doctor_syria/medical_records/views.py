from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from notifications.utils import send_notification
from users.models import Doctor, Patient
from .filters import (
    AllergyFilter,
    MedicalRecordFilter,
    VaccinationFilter,
    MedicalDocumentFilter
)
from .models import (
    Allergy,
    MedicalRecord,
    PatientHistory,
    Vaccination,
    MedicalDocument,
    Diagnosis,
    Treatment,
    Prescription,
    LabResult
)
from .permissions import (
    IsMedicalStaff,
    IsPatientOrMedicalStaff,
    CanViewMedicalRecords
)
from .serializers import (
    AllergySerializer,
    MedicalRecordSerializer,
    PatientHistorySerializer,
    VaccinationSerializer,
    MedicalDocumentSerializer,
    DiagnosisSerializer,
    TreatmentSerializer,
    PrescriptionSerializer,
    LabResultSerializer,
    MedicalRecordDetailSerializer
)
from .utils import (
    generate_pdf_report,
    send_medical_report,
    analyze_medical_history,
    calculate_health_metrics
)


class RecordListView(LoginRequiredMixin, ListView):
    model = MedicalRecord
    template_name = "medical_records/record_list.html"
    context_object_name = "records"
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.role == "doctor":
            return MedicalRecord.objects.filter(doctor=user.doctor)
        elif user.role == "patient":
            return MedicalRecord.objects.filter(patient=user.patient)
        return MedicalRecord.objects.none()


class RecordDetailView(LoginRequiredMixin, DetailView):
    model = MedicalRecord
    template_name = "medical_records/record_detail.html"
    context_object_name = "record"

    def get_queryset(self):
        user = self.request.user
        if user.role == "doctor":
            return MedicalRecord.objects.filter(doctor=user.doctor)
        elif user.role == "patient":
            return MedicalRecord.objects.filter(patient=user.patient)
        return MedicalRecord.objects.none()


class RecordCreateView(LoginRequiredMixin, CreateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = "medical_records/record_form.html"
    success_url = reverse_lazy("medical_records:record_list")

    def form_valid(self, form):
        form.instance.doctor = self.request.user.doctor
        return super().form_valid(form)


class RecordUpdateView(LoginRequiredMixin, UpdateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = "medical_records/record_form.html"
    success_url = reverse_lazy("medical_records:record_list")

    def get_queryset(self):
        return MedicalRecord.objects.filter(doctor=self.request.user.doctor)


class RecordDeleteView(LoginRequiredMixin, DeleteView):
    model = MedicalRecord
    template_name = "medical_records/record_confirm_delete.html"
    success_url = reverse_lazy("medical_records:record_list")

    def get_queryset(self):
        return MedicalRecord.objects.filter(doctor=self.request.user.doctor)


class MedicalRecordViewSet(viewsets.ModelViewSet):
    """ViewSet للسجلات الطبية مع وظائف متقدمة للإدارة والتحليل"""
    permission_classes = [permissions.IsAuthenticated, IsPatientOrMedicalStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MedicalRecordFilter
    search_fields = [
        'title', 'description', 'notes', 'diagnosis__name',
        'patient__user__first_name', 'patient__user__last_name',
        'doctor__user__first_name', 'doctor__user__last_name'
    ]
    ordering_fields = ['date', 'created_at', 'severity', 'last_updated']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MedicalRecordDetailSerializer
        return MedicalRecordSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'doctor'):
            return MedicalRecord.objects.filter(
                Q(doctor=user.doctor) | 
                Q(patient__assigned_doctors=user.doctor)
            ).distinct()
        elif hasattr(user, 'patient'):
            return MedicalRecord.objects.filter(patient=user.patient)
        return MedicalRecord.objects.none()

    def perform_create(self, serializer):
        record = serializer.save(doctor=self.request.user.doctor)
        
        # إرسال إشعار للمريض
        send_notification(
            recipient=record.patient.user,
            title='سجل طبي جديد',
            message=f'تم إضافة سجل طبي جديد بواسطة د. {record.doctor.user.get_full_name()}'
        )

    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        """مشاركة السجل الطبي مع طبيب آخر"""
        record = self.get_object()
        doctor_id = request.data.get('doctor_id')
        if not doctor_id:
            return Response(
                {'error': 'يجب تحديد الطبيب'},
                status=status.HTTP_400_BAD_REQUEST
            )

        doctor = get_object_or_404(Doctor, id=doctor_id)
        record.shared_with.add(doctor)
        
        # إرسال إشعار للطبيب
        send_notification(
            recipient=doctor.user,
            title='مشاركة سجل طبي',
            message=f'تمت مشاركة سجل طبي معك من قبل د. {record.doctor.user.get_full_name()}'
        )

        return Response({'status': 'تمت المشاركة بنجاح'})

    @action(detail=True, methods=['post'])
    def add_diagnosis(self, request, pk=None):
        """إضافة تشخيص للسجل الطبي"""
        record = self.get_object()
        serializer = DiagnosisSerializer(data=request.data)
        if serializer.is_valid():
            diagnosis = serializer.save(
                record=record,
                doctor=self.request.user.doctor
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_treatment(self, request, pk=None):
        """إضافة علاج للسجل الطبي"""
        record = self.get_object()
        serializer = TreatmentSerializer(data=request.data)
        if serializer.is_valid():
            treatment = serializer.save(
                record=record,
                doctor=self.request.user.doctor
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        """عرض التسلسل الزمني للسجل الطبي"""
        record = self.get_object()
        timeline_data = []

        # إضافة التشخيصات
        for diagnosis in record.diagnoses.all():
            timeline_data.append({
                'date': diagnosis.date,
                'type': 'diagnosis',
                'data': DiagnosisSerializer(diagnosis).data
            })

        # إضافة العلاجات
        for treatment in record.treatments.all():
            timeline_data.append({
                'date': treatment.date,
                'type': 'treatment',
                'data': TreatmentSerializer(treatment).data
            })

        # إضافة نتائج المختبر
        for result in record.lab_results.all():
            timeline_data.append({
                'date': result.date,
                'type': 'lab_result',
                'data': LabResultSerializer(result).data
            })

        # ترتيب حسب التاريخ
        timeline_data.sort(key=lambda x: x['date'], reverse=True)
        return Response(timeline_data)

    @action(detail=True, methods=['get'])
    def generate_report(self, request, pk=None):
        """توليد تقرير PDF للسجل الطبي"""
        record = self.get_object()
        pdf = generate_pdf_report(record)
        
        if request.query_params.get('send_email'):
            send_medical_report(record, pdf)
            return Response({'status': 'تم إرسال التقرير بنجاح'})

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="medical_record_{pk}.pdf"'
        return response

    @action(detail=False)
    def statistics(self, request):
        """إحصائيات السجلات الطبية"""
        queryset = self.get_queryset()
        
        # إحصائيات عامة
        total = queryset.count()
        by_severity = queryset.values('severity').annotate(count=Count('id'))
        by_month = queryset.extra(
            select={'month': "EXTRACT(month FROM date)"}
        ).values('month').annotate(count=Count('id'))
        
        # تحليل التشخيصات
        diagnoses = Diagnosis.objects.filter(record__in=queryset)
        common_diagnoses = diagnoses.values('name').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        # تحليل العلاجات
        treatments = Treatment.objects.filter(record__in=queryset)
        common_treatments = treatments.values('name').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        return Response({
            'total_records': total,
            'by_severity': by_severity,
            'by_month': by_month,
            'common_diagnoses': common_diagnoses,
            'common_treatments': common_treatments
        })

    @action(detail=False)
    def search_by_symptoms(self, request):
        """البحث في السجلات حسب الأعراض"""
        symptoms = request.query_params.get('symptoms', '').split(',')
        if not symptoms:
            return Response(
                {'error': 'يجب تحديد الأعراض'},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = self.get_queryset().filter(
            Q(symptoms__name__in=symptoms) |
            Q(notes__icontains=symptoms)
        ).distinct()
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PatientHistoryViewSet(viewsets.ModelViewSet):
    """ViewSet لتاريخ المريض مع وظائف متقدمة للتحليل"""
    serializer_class = PatientHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsPatientOrMedicalStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['notes', 'diagnosis', 'treatment']
    ordering_fields = ['date']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'doctor'):
            return PatientHistory.objects.filter(
                Q(doctor=user.doctor) |
                Q(patient__assigned_doctors=user.doctor)
            ).distinct()
        elif hasattr(user, 'patient'):
            return PatientHistory.objects.filter(patient=user.patient)
        return PatientHistory.objects.none()

    @action(detail=False)
    def analyze(self, request):
        """تحليل التاريخ الطبي للمريض"""
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response(
                {'error': 'يجب تحديد المريض'},
                status=status.HTTP_400_BAD_REQUEST
            )

        patient = get_object_or_404(Patient, id=patient_id)
        analysis = analyze_medical_history(patient)
        metrics = calculate_health_metrics(patient)
        
        return Response({
            'analysis': analysis,
            'metrics': metrics
        })


class AllergyViewSet(viewsets.ModelViewSet):
    """ViewSet للحساسية مع وظائف متقدمة للإدارة"""
    serializer_class = AllergySerializer
    permission_classes = [permissions.IsAuthenticated, IsPatientOrMedicalStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AllergyFilter
    search_fields = ['allergen', 'reaction', 'notes']
    ordering_fields = ['diagnosis_date', 'severity']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'doctor'):
            return Allergy.objects.filter(
                Q(doctor=user.doctor) |
                Q(patient__assigned_doctors=user.doctor)
            ).distinct()
        elif hasattr(user, 'patient'):
            return Allergy.objects.filter(patient=user.patient)
        return Allergy.objects.none()

    def perform_create(self, serializer):
        allergy = serializer.save(doctor=self.request.user.doctor)
        
        # إرسال إشعار للمريض
        send_notification(
            recipient=allergy.patient.user,
            title='حساسية جديدة',
            message=f'تم تسجيل حساسية جديدة بواسطة د. {allergy.doctor.user.get_full_name()}'
        )

    @action(detail=False)
    def active(self, request):
        """الحساسيات النشطة"""
        queryset = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def by_severity(self, request):
        """تصنيف الحساسيات حسب الشدة"""
        queryset = self.get_queryset()
        by_severity = queryset.values('severity').annotate(
            count=Count('id')
        ).order_by('severity')
        return Response(by_severity)


class VaccinationViewSet(viewsets.ModelViewSet):
    """ViewSet للتطعيمات مع وظائف متقدمة للإدارة"""
    serializer_class = VaccinationSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatientOrMedicalStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = VaccinationFilter
    search_fields = ['vaccine_name', 'notes', 'batch_number']
    ordering_fields = ['date_given', 'next_due_date']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'doctor'):
            return Vaccination.objects.filter(
                Q(doctor=user.doctor) |
                Q(patient__assigned_doctors=user.doctor)
            ).distinct()
        elif hasattr(user, 'patient'):
            return Vaccination.objects.filter(patient=user.patient)
        return Vaccination.objects.none()

    def perform_create(self, serializer):
        vaccination = serializer.save(doctor=self.request.user.doctor)
        
        # إرسال إشعار للمريض
        send_notification(
            recipient=vaccination.patient.user,
            title='تطعيم جديد',
            message=f'تم تسجيل تطعيم جديد بواسطة د. {vaccination.doctor.user.get_full_name()}'
        )

    @action(detail=False)
    def due_soon(self, request):
        """التطعيمات المستحقة قريباً"""
        days = int(request.query_params.get('days', 30))
        due_date = timezone.now().date() + timedelta(days=days)
        
        queryset = self.get_queryset().filter(
            next_due_date__lte=due_date,
            next_due_date__gte=timezone.now().date()
        )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def overdue(self, request):
        """التطعيمات المتأخرة"""
        queryset = self.get_queryset().filter(
            next_due_date__lt=timezone.now().date()
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MedicalDocumentViewSet(viewsets.ModelViewSet):
    """ViewSet للوثائق الطبية مع وظائف متقدمة للإدارة"""
    serializer_class = MedicalDocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatientOrMedicalStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MedicalDocumentFilter
    search_fields = ['title', 'description', 'document_type']
    ordering_fields = ['upload_date', 'document_type']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'doctor'):
            return MedicalDocument.objects.filter(
                Q(doctor=user.doctor) |
                Q(patient__assigned_doctors=user.doctor)
            ).distinct()
        elif hasattr(user, 'patient'):
            return MedicalDocument.objects.filter(patient=user.patient)
        return MedicalDocument.objects.none()

    def perform_create(self, serializer):
        document = serializer.save(
            doctor=self.request.user.doctor,
            uploaded_by=self.request.user
        )
        
        # إرسال إشعار للمريض
        send_notification(
            recipient=document.patient.user,
            title='وثيقة طبية جديدة',
            message=f'تم إضافة وثيقة طبية جديدة بواسطة د. {document.doctor.user.get_full_name()}'
        )

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """تحميل الوثيقة الطبية"""
        document = self.get_object()
        response = HttpResponse(document.file, content_type=document.content_type)
        response['Content-Disposition'] = f'attachment; filename="{document.title}"'
        return response

    @action(detail=False)
    def by_type(self, request):
        """تصنيف الوثائق حسب النوع"""
        queryset = self.get_queryset()
        by_type = queryset.values('document_type').annotate(
            count=Count('id')
        ).order_by('document_type')
        return Response(by_type)
