from datetime import time

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from doctor_syria.doctor.models import (
    Doctor,
    DoctorReview,
    DoctorSchedule,
    Prescription,
    Specialization,
)
from patient_records.models import Patient

User = get_user_model()


@pytest.mark.django_db
class TestDoctor:
    @pytest.fixture
    def client(self):
        return Client()

    @pytest.fixture
    def test_user(self):
        return User.objects.create_user(
            username="testdoctor", email="doctor@test.com", password="testpass123"
        )

    @pytest.fixture
    def test_specialization(self):
        return Specialization.objects.create(
            name="Cardiology", description="Heart specialist"
        )

    @pytest.fixture
    def test_doctor(self, test_user, test_specialization):
        return Doctor.objects.create(
            user=test_user,
            specialization=test_specialization,
            license_number="12345",
            years_of_experience=10,
            education="MD from Test University",
        )

    @pytest.fixture
    def test_patient_user(self):
        return User.objects.create_user(
            username="testpatient", email="patient@test.com", password="testpass123"
        )

    @pytest.fixture
    def test_patient(self, test_patient_user):
        return Patient.objects.create(
            user=test_patient_user, date_of_birth="1990-01-01", blood_type="A+"
        )

    def test_create_doctor(self, test_specialization):
        user = User.objects.create_user(
            username="newdoctor", email="new@doctor.com", password="testpass123"
        )
        doctor = Doctor.objects.create(
            user=user,
            specialization=test_specialization,
            license_number="67890",
            years_of_experience=5,
            education="MD from Medical School",
        )
        assert doctor.license_number == "67890"
        assert doctor.years_of_experience == 5

    def test_doctor_schedule(self, test_doctor):
        schedule = DoctorSchedule.objects.create(
            doctor=test_doctor,
            day="Monday",
            start_time=time(9, 0),
            end_time=time(17, 0),
            is_working=True,
        )
        assert schedule.is_working
        assert schedule.start_time == time(9, 0)
        assert schedule.end_time == time(17, 0)

    def test_doctor_availability(self, test_doctor):
        DoctorSchedule.objects.create(
            doctor=test_doctor,
            day="Monday",
            start_time=time(9, 0),
            end_time=time(17, 0),
            is_working=True,
        )
        assert test_doctor.is_available_on("2025-01-13", "10:00")  # Monday
        test_doctor.is_available = False
        test_doctor.save()
        assert not test_doctor.is_available_on("2025-01-13", "10:00")

    def test_prescription(self, test_doctor, test_patient):
        prescription = Prescription.objects.create(
            doctor=test_doctor,
            patient=test_patient,
            diagnosis="Test Condition",
            notes="Test Notes",
        )
        assert prescription.doctor == test_doctor
        assert prescription.patient == test_patient
        assert prescription.is_active

    def test_doctor_review(self, test_doctor, test_patient):
        review = DoctorReview.objects.create(
            doctor=test_doctor,
            patient=test_patient,
            rating=5,
            comment="Excellent doctor",
        )
        assert review.rating == 5
        assert test_doctor.get_rating() == 5.0

    def test_multiple_reviews(self, test_doctor, test_patient):
        # Create another patient for second review
        user2 = User.objects.create_user(
            username="patient2", email="patient2@test.com", password="testpass123"
        )
        patient2 = Patient.objects.create(
            user=user2, date_of_birth="1995-01-01", blood_type="B+"
        )

        DoctorReview.objects.create(
            doctor=test_doctor, patient=test_patient, rating=5, comment="Excellent"
        )
        DoctorReview.objects.create(
            doctor=test_doctor, patient=patient2, rating=4, comment="Very good"
        )
        assert test_doctor.get_rating() == 4.5

    def test_doctor_schedule_validation(self, test_doctor):
        schedule = DoctorSchedule.objects.create(
            doctor=test_doctor,
            day="Monday",
            start_time=time(9, 0),
            end_time=time(17, 0),
            break_start=time(12, 0),
            break_end=time(13, 0),
        )
        assert schedule.is_available_at("10:00")  # During working hours
        assert not schedule.is_available_at("12:30")  # During break
        assert not schedule.is_available_at("08:00")  # Before hours
        assert not schedule.is_available_at("18:00")  # After hours

    def test_specialization_doctors(self, test_specialization, test_doctor):
        assert test_doctor in test_specialization.get_active_doctors()
        test_doctor.is_available = False
        test_doctor.save()
        assert (
            test_doctor in test_specialization.get_active_doctors()
        )  # Still active even if not available
