import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from doctors.models import Doctor
from patient_records.models import Patient
from appointments.models import Appointment, Schedule
from clinics.models import Clinic
from django.utils import timezone

User = get_user_model()

class CoreTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test doctor
        self.doctor = Doctor.objects.create(
            user=self.user,
            specialty=None,  # We'll need to create a Specialty instance if needed
            phone='1234567890',
            address='Test Address',
            bio='Test Bio'
        )
        
        # Create test patient
        self.patient_user = User.objects.create_user(
            username='patient',
            email='patient@example.com',
            password='patient123'
        )
        self.patient = Patient.objects.create(
            user=self.patient_user,
            date_of_birth=timezone.now().date(),
            gender='M',
            marital_status='single',
            phone_number='0987654321',
            emergency_contact_name='Emergency Contact'
        )
        
        # Create test clinic
        self.clinic = Clinic.objects.create(
            name='Test Clinic',
            address='Test Address',
            phone='1234567890'
        )

    def test_user_creation(self):
        """Test user creation"""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))

    def test_doctor_creation(self):
        """Test doctor creation"""
        self.assertEqual(self.doctor.user.username, 'testuser')
        self.assertEqual(self.doctor.phone, '1234567890')

    def test_patient_creation(self):
        """Test patient creation"""
        self.assertEqual(self.patient.user.username, 'patient')
        self.assertEqual(self.patient.gender, 'M')

    def test_clinic_creation(self):
        """Test clinic creation"""
        self.assertEqual(self.clinic.name, 'Test Clinic')
        self.assertEqual(self.clinic.phone, '1234567890')

    def test_appointment_creation(self):
        """Test appointment creation"""
        # Create schedule for doctor
        schedule = Schedule.objects.create(
            doctor=self.doctor,
            day_of_week=0,  # Monday
            start_time='09:00:00',
            end_time='17:00:00',
            appointment_duration=30
        )
        
        appointment_date = timezone.datetime(2025, 1, 20, 10, 0, 0, tzinfo=timezone.utc)  # Monday
        appointment = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            appointment_date=appointment_date,
            reason='Regular checkup',
            status='pending'
        )
        self.assertEqual(appointment.status, 'pending')
        self.assertEqual(appointment.doctor, self.doctor)
        self.assertEqual(appointment.patient, self.patient)
