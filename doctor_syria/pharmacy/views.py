"""
Pharmacy views.
"""
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.permissions import IsPharmacist
from .models import Medicine, Prescription, PrescriptionItem
from .serializers import (
    MedicineSerializer,
    PrescriptionSerializer,
    PrescriptionItemSerializer,
)


class MedicineViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing medicine instances.
    """
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsPharmacist]
    search_fields = ['name', 'name_ar', 'description']
    filterset_fields = ['category', 'form', 'requires_prescription', 'is_active']
    ordering_fields = ['name', 'price', 'quantity']

    def get_queryset(self):
        """
        This view should return a list of all medicines
        for the currently authenticated user.
        """
        return Medicine.objects.filter(is_active=True)


class PrescriptionViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing prescription instances.
    """
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsPharmacist]
    search_fields = ['patient__name', 'notes']
    filterset_fields = ['is_filled']
    ordering_fields = ['created_at']

    def get_queryset(self):
        """
        This view should return a list of all prescriptions
        for the currently authenticated user.
        """
        return Prescription.objects.all()

    @action(detail=True, methods=['post'])
    def fill(self, request, pk=None):
        """
        Fill a prescription.
        """
        prescription = self.get_object()
        if prescription.is_filled:
            return Response(
                {'detail': _('Prescription is already filled.')},
                status=status.HTTP_400_BAD_REQUEST
            )

        prescription.is_filled = True
        prescription.save()

        return Response({'detail': _('Prescription filled successfully.')})


class PrescriptionItemViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing prescription item instances.
    """
    queryset = PrescriptionItem.objects.all()
    serializer_class = PrescriptionItemSerializer
    permission_classes = [IsPharmacist]
    filterset_fields = ['prescription', 'medicine']
    ordering_fields = ['created_at']

    def get_queryset(self):
        """
        This view should return a list of all prescription items
        for the currently authenticated user.
        """
        return PrescriptionItem.objects.all()
