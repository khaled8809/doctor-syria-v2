from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Appointment, Prescription, MedicalRecord
from .serializers import (
    AppointmentSerializer,
    PrescriptionSerializer,
    MedicalRecordSerializer,
)


class AppointmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["status", "appointment_type", "date"]
    search_fields = ["doctor__user__first_name", "patient__user__first_name"]
    ordering_fields = ["date", "time"]

    def get_queryset(self):
        user = self.request.user
        if user.role == "doctor":
            return Appointment.objects.filter(doctor__user=user)
        elif user.role == "patient":
            return Appointment.objects.filter(patient__user=user)
        return Appointment.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == "patient":
            serializer.save(patient=user.patient)
        elif user.role == "doctor":
            serializer.save(doctor=user.doctor)


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "doctor":
            return Appointment.objects.filter(doctor__user=user)
        elif user.role == "patient":
            return Appointment.objects.filter(patient__user=user)
        return Appointment.objects.none()


class PrescriptionListCreateView(generics.ListCreateAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["appointment__date"]
    search_fields = [
        "appointment__doctor__user__first_name",
        "appointment__patient__user__first_name",
    ]
    ordering_fields = ["created_at", "valid_until"]

    def get_queryset(self):
        user = self.request.user
        if user.role == "doctor":
            return Prescription.objects.filter(appointment__doctor__user=user)
        elif user.role == "patient":
            return Prescription.objects.filter(appointment__patient__user=user)
        return Prescription.objects.none()


class PrescriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "doctor":
            return Prescription.objects.filter(appointment__doctor__user=user)
        elif user.role == "patient":
            return Prescription.objects.filter(appointment__patient__user=user)
        return Prescription.objects.none()


class MedicalRecordListCreateView(generics.ListCreateAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["date"]
    search_fields = [
        "doctor__user__first_name",
        "patient__user__first_name",
        "diagnosis",
    ]
    ordering_fields = ["date", "created_at"]

    def get_queryset(self):
        user = self.request.user
        if user.role == "doctor":
            return MedicalRecord.objects.filter(doctor__user=user)
        elif user.role == "patient":
            return MedicalRecord.objects.filter(patient__user=user)
        return MedicalRecord.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == "doctor":
            serializer.save(doctor=user.doctor)


class MedicalRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "doctor":
            return MedicalRecord.objects.filter(doctor__user=user)
        elif user.role == "patient":
            return MedicalRecord.objects.filter(patient__user=user)
        return MedicalRecord.objects.none()
