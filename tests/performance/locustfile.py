"""Module for load testing the Doctor Syria application using Locust."""

import logging
import os
import random

from faker import Faker
from locust import HttpUser, between, task
from locust.exception import StopUser

logger = logging.getLogger(__name__)
fake = Faker("ar_SA")

# Get credentials from environment variables
TEST_USERNAME = os.getenv("TEST_USERNAME", "test_user")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "test_password")


class DoctorSyriaUser(HttpUser):
    """User class for simulating typical user behavior in the application."""

    wait_time = between(1, 5)

    def __init__(self, *args, **kwargs):
        """Initialize the user with authentication token."""
        super().__init__(*args, **kwargs)
        self.token = None

    def on_start(self):
        """Log in when simulation starts."""
        try:
            response = self.client.post(
                "/api/auth/login/", {"username": TEST_USERNAME, "password": TEST_PASSWORD}
            )
            if response.status_code == 200:
                self.token = response.json().get("token")
                if not self.token:
                    logger.error("Login successful but no token received")
                    raise StopUser()
            else:
                logger.error(f"Login failed with status code: {response.status_code}")
                raise StopUser()
        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            raise StopUser()

    def on_stop(self):
        """Cleanup when simulation stops."""
        if self.token:
            try:
                self.client.post("/api/auth/logout/", headers=self._get_headers())
            except Exception as e:
                logger.error(f"Error during logout: {str(e)}")

    def _get_headers(self):
        """Get request headers with authentication token."""
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    @task(3)
    def view_dashboard(self):
        """Simulate viewing the dashboard."""
        try:
            with self.client.get(
                "/api/dashboard/", headers=self._get_headers(), catch_response=True
            ) as response:
                if response.status_code != 200:
                    response.failure(f"Dashboard view failed: {response.status_code}")
        except Exception as e:
            logger.error(f"Error viewing dashboard: {str(e)}")

    @task(2)
    def search_patients(self):
        """Simulate searching for patients."""
        try:
            with self.client.get(
                f"/api/patients/search/?query={fake.name()}",
                headers=self._get_headers(),
                catch_response=True,
            ) as response:
                if response.status_code != 200:
                    response.failure(f"Patient search failed: {response.status_code}")
        except Exception as e:
            logger.error(f"Error searching patients: {str(e)}")

    @task(2)
    def create_appointment(self):
        """Simulate creating a new appointment."""
        try:
            appointment_data = {
                "patient": random.randint(1, 1000),
                "doctor": random.randint(1, 100),
                "appointment_date": fake.future_date().isoformat(),
                "reason": fake.text(),
                "status": "pending",
            }
            with self.client.post(
                "/api/appointments/",
                json=appointment_data,
                headers=self._get_headers(),
                catch_response=True,
            ) as response:
                if response.status_code not in (201, 200):
                    response.failure(f"Appointment creation failed: {response.status_code}")
        except Exception as e:
            logger.error(f"Error creating appointment: {str(e)}")

    @task(1)
    def view_medical_record(self):
        """Simulate viewing a medical record."""
        try:
            record_id = random.randint(1, 1000)
            with self.client.get(
                f"/api/medical-records/{record_id}/",
                headers=self._get_headers(),
                catch_response=True,
            ) as response:
                if response.status_code not in (200, 404):  # 404 is acceptable for random IDs
                    response.failure(f"Medical record view failed: {response.status_code}")
        except Exception as e:
            logger.error(f"Error viewing medical record: {str(e)}")
