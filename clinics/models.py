from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from doctors.models import Doctor
from patient_records.models import Patient


class Clinic(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    description = models.TextField()
    working_hours = models.JSONField(default=dict)
    facilities = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    head_doctor = models.ForeignKey(
        Doctor, on_delete=models.SET_NULL, null=True, related_name="headed_departments"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.clinic.name} - {self.name}"


class ClinicStaff(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="clinic_staff"
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    joined_date = models.DateField()

    def __str__(self):
        return f"{self.clinic.name} - {self.user.get_full_name()}"


class Room(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    number = models.CharField(max_length=20)
    type = models.CharField(max_length=50)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)
    equipment_notes = models.TextField()

    def __str__(self):
        return f"{self.clinic.name} - Room {self.number}"


class Equipment(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="room_equipment"
    )
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    purchase_date = models.DateField()
    warranty_expiry = models.DateField()
    last_maintenance = models.DateField()
    status = models.CharField(max_length=50)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.clinic.name} - {self.name}"


class Visit(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="clinic_visits"
    )
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    visit_date = models.DateTimeField()
    purpose = models.TextField()
    status = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.clinic.name} - {self.patient} - {self.visit_date}"


class ClinicService(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()  # in minutes
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.clinic.name} - {self.name}"


class ServiceBooking(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    service = models.ForeignKey(ClinicService, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="service_bookings"
    )
    booking_date = models.DateTimeField()
    status = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.clinic.name} - {self.service.name} - {self.patient}"
