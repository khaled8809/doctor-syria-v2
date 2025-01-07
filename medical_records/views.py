"""
Views for the medical records app
"""

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from core.cache_decorators import cache_response
from core.cache_manager import CacheManager

# سيتم إضافة المزيد من الـ views لاحقاً

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
