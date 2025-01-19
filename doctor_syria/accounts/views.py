"""
Views for the accounts application.
"""
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response

from .models import Doctor, Laboratory, Patient, Pharmacy, Specialization, Insurance
from .serializers import (
    DoctorSerializer,
    LaboratorySerializer,
    PatientSerializer,
    PharmacySerializer,
    UserSerializer,
    SpecializationSerializer,
    InsuranceSerializer,
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class DoctorListView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ["specialization", "available"]
    search_fields = ["user__first_name", "user__last_name", "specialization"]
    ordering_fields = ["user__first_name", "rating"]


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PharmacyListView(generics.ListCreateAPIView):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ["license_number", "is_24_hours"]
    search_fields = ["user__first_name", "name", "address"]
    ordering_fields = ["name", "rating"]


class PharmacyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class LaboratoryListView(generics.ListCreateAPIView):
    queryset = Laboratory.objects.all()
    serializer_class = LaboratorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ["license_number", "is_24_hours"]
    search_fields = ["user__first_name", "name", "address"]
    ordering_fields = ["name", "rating"]


class LaboratoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Laboratory.objects.all()
    serializer_class = LaboratorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DoctorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing doctors.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]


class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing patients.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]


class SpecializationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing specializations.
    """
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [permissions.IsAuthenticated]


class InsuranceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing insurance information.
    """
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerializer
    permission_classes = [permissions.IsAuthenticated]
