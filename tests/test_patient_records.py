import pytest
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from doctor_syria.doctor.models import Doctor
from patient_records.models import MedicalRecord, Patient, Prescription

User = get_user_model()


@pytest.mark.django_db
class TestPatientRecords:
    @pytest.fixture
    def client(self):
        return Client()

    @pytest.fixture
    def test_user(self):
        return User.objects.create_user(
            username="testpatient", email="patient@test.com", password="testpass123"
        )

    @pytest.fixture
    def test_doctor(self):
        user = User.objects.create_user(
            username="testdoctor", email="doctor@test.com", password="testpass123"
        )
        return Doctor.objects.create(
            user=user, specialization="General", license_number="12345"
        )

    @pytest.fixture
    def test_patient(self, test_user):
        return Patient.objects.create(
            user=test_user,
            date_of_birth="1990-01-01",
            blood_type="A+",
            emergency_contact="1234567890",
        )

    def test_create_medical_record(self, test_patient, test_doctor):
        record = MedicalRecord.objects.create(
            patient=test_patient,
            doctor=test_doctor,
            diagnosis="Common Cold",
            symptoms="Fever, Cough",
            treatment="Rest and Fluids",
        )
        assert record.diagnosis == "Common Cold"
        assert record.patient == test_patient

    def test_create_prescription(self, test_patient, test_doctor):
        prescription = Prescription.objects.create(
            patient=test_patient,
            doctor=test_doctor,
            medication="Paracetamol",
            dosage="500mg",
            frequency="Every 6 hours",
            duration="5 days",
        )
        assert prescription.medication == "Paracetamol"
        assert prescription.patient == test_patient

    def test_update_medical_record(self, test_patient, test_doctor):
        record = MedicalRecord.objects.create(
            patient=test_patient,
            doctor=test_doctor,
            diagnosis="Initial Diagnosis",
            treatment="Initial Treatment",
        )
        record.diagnosis = "Updated Diagnosis"
        record.save()
        assert record.diagnosis == "Updated Diagnosis"

    def test_patient_history(self, test_patient, test_doctor):
        # Create multiple records
        MedicalRecord.objects.create(
            patient=test_patient,
            doctor=test_doctor,
            diagnosis="Past Condition 1",
            date_created="2024-01-01",
        )
        MedicalRecord.objects.create(
            patient=test_patient,
            doctor=test_doctor,
            diagnosis="Past Condition 2",
            date_created="2024-01-02",
        )
        history = MedicalRecord.objects.filter(patient=test_patient)
        assert history.count() == 2

    def test_prescription_validation(self, test_patient, test_doctor):
        with pytest.raises(ValueError):
            Prescription.objects.create(
                patient=test_patient,
                doctor=test_doctor,
                medication="",  # Empty medication
                dosage="500mg",
            )
