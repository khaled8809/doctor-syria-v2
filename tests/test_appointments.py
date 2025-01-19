import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from appointments.models import Schedule


@pytest.mark.django_db
class TestAppointmentAPI:
    @pytest.fixture
    def doctor_schedule(self, create_user):
        doctor = create_user(is_staff=True)
        schedule = Schedule.objects.create(
            doctor=doctor,
            day_of_week=timezone.now().weekday(),
            start_time="09:00",
            end_time="17:00",
            appointment_duration=30,
            is_available=True,
        )
        return doctor, schedule

    def test_create_appointment(self, auto_login_user, doctor_schedule):
        client, user = auto_login_user()
        doctor, schedule = doctor_schedule
        url = reverse("appointment-list")

        appointment_date = timezone.now().replace(
            hour=10, minute=0, second=0, microsecond=0
        ) + timezone.timedelta(days=1)

        data = {
            "doctor": doctor.id,
            "appointment_date": appointment_date.isoformat(),
            "reason": "Regular checkup",
            "priority": "normal",
        }

        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["status"] == "pending"
        assert response.data["doctor"] == doctor.id
        assert response.data["patient"] == user.id

    def test_list_appointments(self, auto_login_user, doctor_schedule):
        client, user = auto_login_user()
        url = reverse("appointment-list")

        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_get_appointment_detail(self, auto_login_user, doctor_schedule):
        client, user = auto_login_user()
        doctor, schedule = doctor_schedule

        # First create an appointment
        create_url = reverse("appointment-list")
        appointment_date = timezone.now().replace(
            hour=10, minute=0, second=0, microsecond=0
        ) + timezone.timedelta(days=1)

        data = {
            "doctor": doctor.id,
            "appointment_date": appointment_date.isoformat(),
            "reason": "Regular checkup",
            "priority": "normal",
        }

        create_response = client.post(create_url, data)
        appointment_id = create_response.data["id"]

        # Then get its details
        url = reverse("appointment-detail", kwargs={"pk": appointment_id})
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["reason"] == data["reason"]
        assert response.data["doctor"] == doctor.id

    def test_update_appointment(self, auto_login_user, doctor_schedule):
        client, user = auto_login_user()
        doctor, schedule = doctor_schedule

        # First create an appointment
        create_url = reverse("appointment-list")
        appointment_date = timezone.now().replace(
            hour=10, minute=0, second=0, microsecond=0
        ) + timezone.timedelta(days=1)

        data = {
            "doctor": doctor.id,
            "appointment_date": appointment_date.isoformat(),
            "reason": "Regular checkup",
            "priority": "normal",
        }

        create_response = client.post(create_url, data)
        appointment_id = create_response.data["id"]

        # Then update it
        url = reverse("appointment-detail", kwargs={"pk": appointment_id})
        new_date = timezone.now().replace(
            hour=14, minute=0, second=0, microsecond=0
        ) + timezone.timedelta(days=2)

        update_data = {
            "doctor": doctor.id,
            "appointment_date": new_date.isoformat(),
            "reason": "Follow-up",
            "priority": "urgent",
        }

        response = client.put(url, update_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["reason"] == update_data["reason"]
        assert response.data["priority"] == update_data["priority"]

    def test_cancel_appointment(self, auto_login_user, doctor_schedule):
        client, user = auto_login_user()
        doctor, schedule = doctor_schedule

        # First create an appointment
        create_url = reverse("appointment-list")
        appointment_date = timezone.now().replace(
            hour=10, minute=0, second=0, microsecond=0
        ) + timezone.timedelta(days=1)

        data = {
            "doctor": doctor.id,
            "appointment_date": appointment_date.isoformat(),
            "reason": "Regular checkup",
            "priority": "normal",
        }

        create_response = client.post(create_url, data)
        appointment_id = create_response.data["id"]

        # Then cancel it
        url = reverse("appointment-cancel", kwargs={"pk": appointment_id})
        response = client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "cancelled"

        # Try to update cancelled appointment
        update_url = reverse("appointment-detail", kwargs={"pk": appointment_id})
        update_data = {"reason": "Changed my mind"}
        response = client.patch(update_url, update_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_reschedule_appointment(self, auto_login_user, doctor_schedule):
        client, user = auto_login_user()
        doctor, schedule = doctor_schedule

        # First create an appointment
        create_url = reverse("appointment-list")
        appointment_date = timezone.now().replace(
            hour=10, minute=0, second=0, microsecond=0
        ) + timezone.timedelta(days=1)

        data = {
            "doctor": doctor.id,
            "appointment_date": appointment_date.isoformat(),
            "reason": "Regular checkup",
            "priority": "normal",
        }

        create_response = client.post(create_url, data)
        appointment_id = create_response.data["id"]

        # Then reschedule it
        url = reverse("appointment-reschedule", kwargs={"pk": appointment_id})
        new_date = timezone.now().replace(
            hour=14, minute=0, second=0, microsecond=0
        ) + timezone.timedelta(days=2)

        reschedule_data = {"appointment_date": new_date.isoformat()}

        response = client.post(url, reschedule_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["appointment_date"] == reschedule_data["appointment_date"]
