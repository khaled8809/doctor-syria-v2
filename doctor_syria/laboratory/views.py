from datetime import timedelta

from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    LabTest,
    ReferenceRange,
    SampleCollection,
    TestCategory,
    TestRequest,
    TestResult,
    Laboratory
)
from .serializers import (
    LabTestSerializer,
    ReferenceRangeSerializer,
    SampleCollectionSerializer,
    TestCategorySerializer,
    TestRequestSerializer,
    TestResultSerializer,
    LaboratorySerializer
)
from .utils import generate_test_report, send_notification


class LabTestViewSet(viewsets.ModelViewSet):
    """ViewSet للفحوصات المخبرية مع وظائف متقدمة"""
    serializer_class = LabTestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["category", "requires_fasting", "is_active"]
    search_fields = ["name", "code", "category__name", "description"]
    ordering_fields = ["name", "price", "created_at", "turnaround_time"]

    def get_queryset(self):
        user = self.request.user
        if user.role == "laboratory":
            return LabTest.objects.all()
        return LabTest.objects.filter(is_active=True)

    @action(detail=False)
    def statistics(self, request):
        """إحصائيات الفحوصات"""
        queryset = self.get_queryset()
        total_tests = queryset.count()
        by_category = queryset.values('category__name').annotate(count=Count('id'))
        most_requested = queryset.annotate(
            request_count=Count('test_requests')
        ).order_by('-request_count')[:5]

        return Response({
            'total_tests': total_tests,
            'by_category': by_category,
            'most_requested': LabTestSerializer(most_requested, many=True).data
        })


class TestCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet لفئات الفحوصات"""
    serializer_class = TestCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]

    def get_queryset(self):
        if self.request.user.role == "laboratory":
            return TestCategory.objects.all()
        return TestCategory.objects.filter(is_active=True)


class TestRequestViewSet(viewsets.ModelViewSet):
    """ViewSet لطلبات الفحص مع وظائف متقدمة للمعالجة والتتبع"""
    serializer_class = TestRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["status", "priority", "requires_fasting"]
    search_fields = [
        "patient__user__first_name",
        "patient__user__last_name",
        "doctor__user__first_name",
        "reference_number"
    ]
    ordering_fields = ["requested_date", "appointment_date", "status", "priority"]

    def get_queryset(self):
        user = self.request.user
        if user.role == "laboratory":
            return TestRequest.objects.filter(laboratory__user=user)
        elif user.role == "doctor":
            return TestRequest.objects.filter(doctor__user=user)
        elif user.role == "patient":
            return TestRequest.objects.filter(patient__user=user)
        return TestRequest.objects.none()

    def perform_create(self, serializer):
        # تعيين المختبر تلقائياً إذا كان المستخدم من المختبر
        if self.request.user.role == "laboratory":
            serializer.save(laboratory=self.request.user.laboratory)
        else:
            serializer.save()

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """إلغاء طلب الفحص"""
        test_request = self.get_object()
        if test_request.status == 'pending':
            test_request.status = 'cancelled'
            test_request.save()
            
            # إرسال إشعار للمريض
            send_notification(
                test_request.patient.user,
                'تم إلغاء طلب الفحص',
                f'تم إلغاء طلب الفحص رقم {test_request.reference_number}'
            )
            
            return Response({'status': 'تم إلغاء طلب الفحص'})
        return Response(
            {'error': 'لا يمكن إلغاء هذا الطلب في حالته الحالية'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def schedule(self, request, pk=None):
        """جدولة موعد للفحص"""
        test_request = self.get_object()
        appointment_date = request.data.get('appointment_date')
        
        if not appointment_date:
            return Response(
                {'error': 'يجب تحديد موعد للفحص'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        test_request.appointment_date = appointment_date
        test_request.status = 'scheduled'
        test_request.save()
        
        # إرسال إشعار للمريض
        send_notification(
            test_request.patient.user,
            'تم جدولة موعد الفحص',
            f'تم تحديد موعد الفحص رقم {test_request.reference_number} في {appointment_date}'
        )
        
        return Response({'status': 'تم جدولة موعد الفحص'})

    @action(detail=False)
    def today(self, request):
        """طلبات الفحص لليوم الحالي"""
        today = timezone.now().date()
        queryset = self.get_queryset().filter(appointment_date__date=today)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TestResultViewSet(viewsets.ModelViewSet):
    """ViewSet لنتائج الفحوصات مع وظائف متقدمة للتحليل والتقارير"""
    serializer_class = TestResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["is_normal", "is_critical", "reviewed"]
    search_fields = [
        "test_request__patient__user__first_name",
        "test_request__reference_number"
    ]
    ordering_fields = ["result_date", "is_critical", "reviewed"]

    def get_queryset(self):
        user = self.request.user
        if user.role == "laboratory":
            return TestResult.objects.filter(test_request__laboratory__user=user)
        elif user.role == "doctor":
            return TestResult.objects.filter(test_request__doctor__user=user)
        elif user.role == "patient":
            return TestResult.objects.filter(test_request__patient__user=user)
        return TestResult.objects.none()

    @action(detail=True)
    def generate_report(self, request, pk=None):
        """توليد تقرير PDF للنتيجة"""
        result = self.get_object()
        pdf = generate_test_report(result)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="test_result_{result.id}.pdf"'
        return response

    @action(detail=True, methods=['post'])
    def mark_reviewed(self, request, pk=None):
        """تحديد النتيجة كمراجعة"""
        result = self.get_object()
        if not result.reviewed:
            result.reviewed = True
            result.reviewed_by = request.user
            result.reviewed_at = timezone.now()
            result.save()
            return Response({'status': 'تم تحديد النتيجة كمراجعة'})
        return Response(
            {'error': 'تم مراجعة هذه النتيجة مسبقاً'},
            status=status.HTTP_400_BAD_REQUEST
        )


class SampleCollectionViewSet(viewsets.ModelViewSet):
    """ViewSet لجمع العينات مع وظائف متقدمة للتتبع"""
    serializer_class = SampleCollectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["status", "is_rejected", "collection_method"]
    search_fields = [
        "test_request__patient__user__first_name",
        "test_request__reference_number",
        "collector__first_name"
    ]
    ordering_fields = ["collection_date", "status", "rejection_date"]

    def get_queryset(self):
        user = self.request.user
        if user.role == "laboratory":
            return SampleCollection.objects.filter(test_request__laboratory__user=user)
        elif user.role == "doctor":
            return SampleCollection.objects.filter(test_request__doctor__user=user)
        elif user.role == "patient":
            return SampleCollection.objects.filter(test_request__patient__user=user)
        return SampleCollection.objects.none()

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """رفض العينة"""
        sample = self.get_object()
        reason = request.data.get('reason')
        
        if not reason:
            return Response(
                {'error': 'يجب تحديد سبب الرفض'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        sample.is_rejected = True
        sample.rejection_reason = reason
        sample.rejection_date = timezone.now()
        sample.status = 'rejected'
        sample.save()
        
        # إرسال إشعار للمريض
        send_notification(
            sample.test_request.patient.user,
            'تم رفض العينة',
            f'تم رفض العينة للفحص رقم {sample.test_request.reference_number}. السبب: {reason}'
        )
        
        return Response({'status': 'تم رفض العينة'})

    @action(detail=True, methods=['post'])
    def collect(self, request, pk=None):
        """جمع العينة"""
        sample = self.get_object()
        if sample.status == 'pending':
            sample.status = 'collected'
            sample.collection_date = timezone.now()
            sample.collector = request.user
            sample.save()
            
            # إرسال إشعار للمريض
            send_notification(
                sample.test_request.patient.user,
                'تم جمع العينة',
                f'تم جمع العينة للفحص رقم {sample.test_request.reference_number}'
            )
            
            return Response({'status': 'تم جمع العينة'})
        return Response(
            {'error': 'لا يمكن جمع هذه العينة في حالتها الحالية'},
            status=status.HTTP_400_BAD_REQUEST
        )


class ReferenceRangeViewSet(viewsets.ModelViewSet):
    """ViewSet للقيم المرجعية"""
    serializer_class = ReferenceRangeSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["test__name", "gender", "age_group"]
    ordering_fields = ["test__name", "min_value", "max_value"]

    def get_queryset(self):
        if self.request.user.role == "laboratory":
            return ReferenceRange.objects.all()
        return ReferenceRange.objects.filter(is_active=True)


class LaboratoryViewSet(viewsets.ModelViewSet):
    """ViewSet للمختبرات"""
    serializer_class = LaboratorySerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["name", "location", "specialization"]
    ordering_fields = ["name", "rating", "test_count"]

    def get_queryset(self):
        if self.request.user.role == "laboratory":
            return Laboratory.objects.all()
        return Laboratory.objects.filter(is_active=True)

    @action(detail=False)
    def statistics(self, request):
        """إحصائيات المختبر"""
        if request.user.role != "laboratory":
            return Response(
                {'error': 'غير مصرح لك بالوصول إلى هذه الإحصائيات'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        laboratory = request.user.laboratory
        today = timezone.now().date()
        
        # إحصائيات اليوم
        today_stats = {
            'total_requests': TestRequest.objects.filter(
                laboratory=laboratory,
                requested_date__date=today
            ).count(),
            'completed_tests': TestResult.objects.filter(
                test_request__laboratory=laboratory,
                result_date__date=today
            ).count(),
            'pending_samples': SampleCollection.objects.filter(
                test_request__laboratory=laboratory,
                status='pending'
            ).count(),
            'critical_results': TestResult.objects.filter(
                test_request__laboratory=laboratory,
                result_date__date=today,
                is_critical=True
            ).count()
        }
        
        # إحصائيات الأسبوع
        week_ago = today - timedelta(days=7)
        weekly_tests = TestResult.objects.filter(
            test_request__laboratory=laboratory,
            result_date__gte=week_ago
        ).count()
        
        return Response({
            'today': today_stats,
            'weekly_tests': weekly_tests,
            'total_tests': laboratory.test_count,
            'average_rating': laboratory.rating
        })
