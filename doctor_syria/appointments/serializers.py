"""
Serializers for the appointments application.
"""
from rest_framework import serializers
from django.utils import timezone
from accounts.serializers import DoctorSerializer, PatientSerializer
from accounts.models import Doctor, Patient
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Appointment model.
    """
    doctor = DoctorSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    doctor_id = serializers.IntegerField(write_only=True)
    patient_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'doctor', 'patient', 'doctor_id', 'patient_id',
            'date', 'duration', 'status', 'reason', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_date(self, value):
        """
        Validate that the appointment date is not in the past.
        """
        if value < timezone.now():
            raise serializers.ValidationError("لا يمكن تحديد موعد في الماضي")
        return value

    def validate(self, data):
        """
        Validate that the doctor and patient exist.
        """
        doctor_id = data.get('doctor_id')
        patient_id = data.get('patient_id')

        try:
            doctor = Doctor.objects.get(id=doctor_id)
            patient = Patient.objects.get(id=patient_id)
        except (Doctor.DoesNotExist, Patient.DoesNotExist):
            raise serializers.ValidationError("الطبيب أو المريض غير موجود")

        # Check if there is an overlapping appointment
        overlapping = Appointment.objects.filter(
            doctor=doctor,
            date=data['date'],
            status__in=['pending', 'confirmed']
        ).exists()

        if overlapping:
            raise serializers.ValidationError("الطبيب لديه موعد آخر في نفس الوقت")

        return data
