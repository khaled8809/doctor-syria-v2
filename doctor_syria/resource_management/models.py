from django.conf import settings
from django.db import models


class MedicalEquipment(models.Model):
    name = models.CharField(max_length=200)
    equipment_type = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(
        "hms.Department", on_delete=models.SET_NULL, null=True
    )
    status = models.CharField(
        max_length=50,
        choices=[
            ("available", "Available"),
            ("in_use", "In Use"),
            ("maintenance", "Under Maintenance"),
            ("out_of_order", "Out of Order"),
        ],
    )
    last_maintenance = models.DateField(null=True, blank=True)
    next_maintenance = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.serial_number})"


class OperatingRoom(models.Model):
    room_number = models.CharField(max_length=50)
    department = models.ForeignKey("hms.Department", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=[
            ("available", "Available"),
            ("occupied", "Occupied"),
            ("cleaning", "Being Cleaned"),
            ("maintenance", "Under Maintenance"),
        ],
    )
    equipment = models.ManyToManyField(MedicalEquipment, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"OR {self.room_number} - {self.department}"


class BedManagement(models.Model):
    bed_number = models.CharField(max_length=50)
    ward = models.ForeignKey("hms.Ward", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=[
            ("available", "Available"),
            ("occupied", "Occupied"),
            ("reserved", "Reserved"),
            ("maintenance", "Under Maintenance"),
        ],
    )
    patient = models.ForeignKey(
        "accounts.Patient", on_delete=models.SET_NULL, null=True, blank=True
    )
    admission_date = models.DateTimeField(null=True, blank=True)
    expected_discharge = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Bed {self.bed_number} - {self.ward}"


class MaintenanceRequest(models.Model):
    equipment = models.ForeignKey(MedicalEquipment, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(
        max_length=50,
        choices=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
            ("urgent", "Urgent"),
        ],
    )
    description = models.TextField()
    status = models.CharField(
        max_length=50,
        choices=[
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
    )
    completion_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Maintenance for {self.equipment} - {self.status}"
