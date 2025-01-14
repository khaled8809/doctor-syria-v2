"""Module for load testing the Doctor Syria application using Locust."""

import random

from faker import Faker
from locust import HttpUser, between, task

fake = Faker("ar_SA")


class DoctorSyriaUser(HttpUser):
    """User class for simulating typical user behavior in the application."""

    wait_time = between(1, 5)

    def on_start(self):
        """Log in when simulation starts."""
        self.client.post("/api/auth/login/", {"username": "test_user", "password": "test_password"})

    @task(3)
    def view_dashboard(self):
        """Simulate viewing the dashboard."""
        self.client.get("/api/dashboard/")

    @task(2)
    def search_patients(self):
        """Simulate searching for patients."""
        self.client.get(f"/api/patients/search/?query={fake.name()}")

    @task(2)
    def create_appointment(self):
        """Simulate creating a new appointment."""
        appointment_data = {
            "patient": random.randint(1, 1000),
            "doctor": random.randint(1, 100),
            "appointment_date": fake.future_date().isoformat(),
            "reason": fake.text(),
            "status": "pending",
        }
        self.client.post("/api/appointments/", json=appointment_data)

    @task(1)
    def view_medical_record(self):
        """Simulate viewing a medical record."""
        record_id = random.randint(1, 1000)
        self.client.get(f"/api/medical-records/{record_id}/")
