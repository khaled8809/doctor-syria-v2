import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from appointments.models import Appointment
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user():
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )

@pytest.fixture
def test_appointment(test_user):
    return Appointment.objects.create(
        patient=test_user,
        appointment_date='2025-01-20',
        appointment_time='10:00:00',
        reason='Regular checkup',
        status='scheduled'
    )

@pytest.mark.django_db
class TestAppointmentAPI:
    def test_create_appointment(self, api_client, test_user):
        api_client.force_authenticate(user=test_user)
        url = reverse('appointment-create')
        data = {
            'appointment_date': '2025-01-20',
            'appointment_time': '10:00:00',
            'reason': 'Regular checkup',
            'status': 'scheduled'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Appointment.objects.count() == 1

    def test_list_appointments(self, api_client, test_user, test_appointment):
        api_client.force_authenticate(user=test_user)
        url = reverse('appointment-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_update_appointment(self, api_client, test_user, test_appointment):
        api_client.force_authenticate(user=test_user)
        url = reverse('appointment-detail', kwargs={'pk': test_appointment.pk})
        data = {'status': 'completed'}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'completed'

    def test_delete_appointment(self, api_client, test_user, test_appointment):
        api_client.force_authenticate(user=test_user)
        url = reverse('appointment-detail', kwargs={'pk': test_appointment.pk})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Appointment.objects.count() == 0

    def test_unauthorized_access(self, api_client):
        url = reverse('appointment-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
