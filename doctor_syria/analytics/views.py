from datetime import timedelta

from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from appointments.models import Appointment
from laboratory.models import LabTest, TestRequest
from medical_records.models import MedicalRecord, Prescription
from pharmacy.models import Medicine, Order
from users.models import User, Doctor, Patient

from .serializers import (
    AppointmentAnalyticsSerializer,
    LabAnalyticsSerializer,
    MedicineAnalyticsSerializer,
    RevenueAnalyticsSerializer,
    UserAnalyticsSerializer
)
from .permissions import IsAdminOrAnalyst


class DashboardViewSet(viewsets.ViewSet):
    """ViewSet للوحة التحكم الرئيسية"""
    permission_classes = [permissions.IsAuthenticated, IsAdminOrAnalyst]

    def list(self, request):
        """إحصائيات عامة للوحة التحكم"""
        today = timezone.now()
        last_month = today - timedelta(days=30)
        
        # إحصائيات المستخدمين
        total_patients = Patient.objects.count()
        total_doctors = Doctor.objects.count()
        new_patients = Patient.objects.filter(created_at__gte=last_month).count()
        
        # إحصائيات المواعيد
        total_appointments = Appointment.objects.count()
        pending_appointments = Appointment.objects.filter(status='pending').count()
        today_appointments = Appointment.objects.filter(
            date=today.date()
        ).count()
        
        # إحصائيات المختبر
        total_tests = LabTest.objects.count()
        pending_tests = TestRequest.objects.filter(status='pending').count()
        
        # إحصائيات الصيدلية
        total_medicines = Medicine.objects.count()
        low_stock_medicines = Medicine.objects.filter(
            quantity__lte=F('minimum_stock')
        ).count()
        
        return Response({
            'users': {
                'total_patients': total_patients,
                'total_doctors': total_doctors,
                'new_patients': new_patients
            },
            'appointments': {
                'total': total_appointments,
                'pending': pending_appointments,
                'today': today_appointments
            },
            'laboratory': {
                'total_tests': total_tests,
                'pending_tests': pending_tests
            },
            'pharmacy': {
                'total_medicines': total_medicines,
                'low_stock': low_stock_medicines
            }
        })


class AppointmentAnalyticsViewSet(viewsets.ViewSet):
    """ViewSet لتحليلات المواعيد"""
    permission_classes = [permissions.IsAuthenticated, IsAdminOrAnalyst]
    serializer_class = AppointmentAnalyticsSerializer

    @action(detail=False)
    def by_department(self, request):
        """تحليل المواعيد حسب القسم"""
        appointments = Appointment.objects.values('department__name').annotate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='completed')),
            cancelled=Count('id', filter=Q(status='cancelled')),
            no_show=Count('id', filter=Q(status='no_show'))
        )
        return Response(appointments)

    @action(detail=False)
    def by_doctor(self, request):
        """تحليل المواعيد حسب الطبيب"""
        appointments = Appointment.objects.values(
            'doctor__user__first_name',
            'doctor__user__last_name'
        ).annotate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='completed')),
            cancelled=Count('id', filter=Q(status='cancelled')),
            avg_duration=Avg('duration')
        )
        return Response(appointments)

    @action(detail=False)
    def time_analysis(self, request):
        """تحليل المواعيد حسب الوقت"""
        today = timezone.now()
        appointments = Appointment.objects.filter(
            date__gte=today - timedelta(days=30)
        ).values('date').annotate(
            total=Count('id'),
            morning=Count('id', filter=Q(time_slot__lt='12:00:00')),
            afternoon=Count('id', filter=Q(time_slot__gte='12:00:00'))
        )
        return Response(appointments)


class LabAnalyticsViewSet(viewsets.ViewSet):
    """ViewSet لتحليلات المختبر"""
    permission_classes = [permissions.IsAuthenticated, IsAdminOrAnalyst]
    serializer_class = LabAnalyticsSerializer

    @action(detail=False)
    def test_statistics(self, request):
        """إحصائيات الفحوصات"""
        tests = TestRequest.objects.values('test__name').annotate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='completed')),
            cancelled=Count('id', filter=Q(status='cancelled')),
            avg_processing_time=Avg('completed_at') - Avg('created_at')
        )
        return Response(tests)

    @action(detail=False)
    def sample_analysis(self, request):
        """تحليل العينات"""
        samples = TestRequest.objects.values('sample_type').annotate(
            total=Count('id'),
            rejected=Count('id', filter=Q(sample_status='rejected')),
            accepted=Count('id', filter=Q(sample_status='accepted'))
        )
        return Response(samples)


class MedicineAnalyticsViewSet(viewsets.ViewSet):
    """ViewSet لتحليلات الأدوية"""
    permission_classes = [permissions.IsAuthenticated, IsAdminOrAnalyst]
    serializer_class = MedicineAnalyticsSerializer

    @action(detail=False)
    def inventory_analysis(self, request):
        """تحليل المخزون"""
        medicines = Medicine.objects.values('category__name').annotate(
            total_items=Count('id'),
            total_quantity=Sum('quantity'),
            low_stock=Count('id', filter=Q(quantity__lte=F('minimum_stock'))),
            out_of_stock=Count('id', filter=Q(quantity=0))
        )
        return Response(medicines)

    @action(detail=False)
    def sales_analysis(self, request):
        """تحليل المبيعات"""
        today = timezone.now()
        orders = Order.objects.filter(
            created_at__gte=today - timedelta(days=30)
        ).values('medicine__name').annotate(
            total_sales=Count('id'),
            total_quantity=Sum('quantity'),
            total_revenue=Sum('total_price')
        )
        return Response(orders)


class RevenueAnalyticsViewSet(viewsets.ViewSet):
    """ViewSet لتحليلات الإيرادات"""
    permission_classes = [permissions.IsAuthenticated, IsAdminOrAnalyst]
    serializer_class = RevenueAnalyticsSerializer

    @action(detail=False)
    def revenue_by_department(self, request):
        """الإيرادات حسب القسم"""
        departments = Appointment.objects.values('department__name').annotate(
            total_revenue=Sum('fee'),
            appointment_count=Count('id'),
            avg_fee=Avg('fee')
        )
        return Response(departments)

    @action(detail=False)
    def revenue_by_service(self, request):
        """الإيرادات حسب الخدمة"""
        # المواعيد
        appointment_revenue = Appointment.objects.aggregate(
            total=Sum('fee'),
            count=Count('id')
        )
        
        # الفحوصات المخبرية
        lab_revenue = TestRequest.objects.aggregate(
            total=Sum('test__price'),
            count=Count('id')
        )
        
        # الأدوية
        pharmacy_revenue = Order.objects.aggregate(
            total=Sum('total_price'),
            count=Count('id')
        )
        
        return Response({
            'appointments': appointment_revenue,
            'laboratory': lab_revenue,
            'pharmacy': pharmacy_revenue
        })


class UserAnalyticsViewSet(viewsets.ViewSet):
    """ViewSet لتحليلات المستخدمين"""
    permission_classes = [permissions.IsAuthenticated, IsAdminOrAnalyst]
    serializer_class = UserAnalyticsSerializer

    @action(detail=False)
    def patient_demographics(self, request):
        """التركيبة السكانية للمرضى"""
        patients = Patient.objects.values('gender', 'age_group').annotate(
            count=Count('id')
        )
        return Response(patients)

    @action(detail=False)
    def doctor_statistics(self, request):
        """إحصائيات الأطباء"""
        doctors = Doctor.objects.values(
            'department__name',
            'specialization'
        ).annotate(
            count=Count('id'),
            avg_appointments=Count('appointments') / Count('id', distinct=True)
        )
        return Response(doctors)

    @action(detail=False)
    def user_activity(self, request):
        """نشاط المستخدمين"""
        today = timezone.now()
        users = User.objects.filter(
            last_login__gte=today - timedelta(days=30)
        ).values('date_joined').annotate(
            total=Count('id'),
            active=Count('id', filter=Q(is_active=True)),
            staff=Count('id', filter=Q(is_staff=True))
        )
        return Response(users)
