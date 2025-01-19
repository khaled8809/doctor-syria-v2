import unittest

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from appointments.models import Appointment
from clinics.models import Clinic
from doctor_syria.doctor.models import Doctor
from patient_records.models import Patient

User = get_user_model()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def test_user():
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )


@pytest.fixture
def test_doctor(test_user):
    return Doctor.objects.create(
        user=test_user,
        specialization="Cardiology",
        license_number="12345",
        years_of_experience=5,
    )


@pytest.fixture
def test_clinic():
    return Clinic.objects.create(
        name="Test Clinic", address="123 Test St", phone="1234567890"
    )


@pytest.fixture
def test_patient(test_user):
    return Patient.objects.create(
        user=test_user, date_of_birth="1990-01-01", blood_type="A+"
    )


@pytest.mark.django_db
class TestAuthentication:
    def test_user_login(self, client):
        User.objects.create_user(username="testuser", password="testpass123")
        response = client.post(
            reverse("login"), {"username": "testuser", "password": "testpass123"}
        )
        assert response.status_code == 302

    def test_user_registration(self, client):
        response = client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "password1": "newpass123",
                "password2": "newpass123",
            },
        )
        assert response.status_code == 302
        assert User.objects.filter(username="newuser").exists()


@pytest.mark.django_db
class TestAppointments:
    def test_create_appointment(self, test_doctor, test_patient):
        appointment = Appointment.objects.create(
            doctor=test_doctor,
            patient=test_patient,
            date="2025-02-01",
            time="10:00:00",
            reason="Regular checkup",
        )
        assert appointment.doctor == test_doctor
        assert appointment.patient == test_patient

    def test_cancel_appointment(self, test_doctor, test_patient):
        appointment = Appointment.objects.create(
            doctor=test_doctor, patient=test_patient, date="2025-02-01", time="10:00:00"
        )
        appointment.status = "cancelled"
        appointment.save()
        assert appointment.status == "cancelled"


@pytest.mark.django_db
class TestClinic:
    def test_create_clinic(self):
        clinic = Clinic.objects.create(
            name="New Clinic", address="456 New St", phone="0987654321"
        )
        assert clinic.name == "New Clinic"
        assert Clinic.objects.filter(name="New Clinic").exists()

    def test_add_doctor_to_clinic(self, test_doctor):
        clinic = Clinic.objects.create(
            name="Doctor Clinic", address="789 Doc St", phone="1122334455"
        )
        clinic.doctors.add(test_doctor)
        assert test_doctor in clinic.doctors.all()


@pytest.mark.django_db
class TestDoctor:
    def test_create_doctor(self, test_user):
        doctor = Doctor.objects.create(
            user=test_user,
            specialization="Pediatrics",
            license_number="67890",
            years_of_experience=10,
        )
        assert doctor.specialization == "Pediatrics"
        assert doctor.license_number == "67890"

    def test_doctor_availability(self, test_doctor):
        test_doctor.is_available = False
        test_doctor.save()
        assert not test_doctor.is_available


class SampleTest(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(1 + 1, 2)

    def test_subtraction(self):
        self.assertEqual(2 - 1, 1)


if __name__ == "__main__":
    unittest.main()
