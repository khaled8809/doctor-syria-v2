from rest_framework import serializers
from .models import Appointment, Prescription, PrescriptionMedicine, MedicalRecord
from accounts.serializers import DoctorSerializer, PatientSerializer


class PrescriptionMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionMedicine
        fields = "__all__"


class PrescriptionSerializer(serializers.ModelSerializer):
    medicines = PrescriptionMedicineSerializer(many=True, read_only=True)

    class Meta:
        model = Prescription
        fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    prescription = PrescriptionSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"

    def validate(self, data):
        # Add validation logic here (e.g., check if doctor is available at the given time)
        return data


class MedicalRecordSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = MedicalRecord
        fields = "__all__"
