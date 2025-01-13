from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from accounts.models import Doctor, Hospital, Nurse, Patient, Staff


class Department(models.Model):
    """الأقسام"""

    DEPARTMENT_TYPES = [
        ("medical", "طبي"),
        ("surgical", "جراحي"),
        ("emergency", "طوارئ"),
        ("icu", "عناية مركزة"),
        ("radiology", "أشعة"),
        ("laboratory", "مختبر"),
        ("pharmacy", "صيدلية"),
        ("physiotherapy", "علاج طبيعي"),
        ("administrative", "إداري"),
    ]

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    department_type = models.CharField(max_length=20, choices=DEPARTMENT_TYPES)
    head_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    capacity = models.PositiveIntegerField()
    floor = models.CharField(max_length=50)
    extension_number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.hospital.name}"


class Ward(models.Model):
    """الأجنحة"""

    WARD_TYPES = [
        ("general", "عام"),
        ("private", "خاص"),
        ("isolation", "عزل"),
        ("pediatric", "أطفال"),
        ("maternity", "ولادة"),
        ("psychiatric", "نفسي"),
    ]

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    ward_type = models.CharField(max_length=20, choices=WARD_TYPES)
    floor = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    current_occupancy = models.PositiveIntegerField(default=0)
    head_nurse = models.ForeignKey(Nurse, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.department.name}"


class Room(models.Model):
    """الغرف"""

    ROOM_TYPES = [
        ("standard", "عادية"),
        ("private", "خاصة"),
        ("suite", "جناح"),
        ("isolation", "عزل"),
        ("icu", "عناية مركزة"),
    ]

    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=50)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    capacity = models.PositiveIntegerField()
    current_occupancy = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    equipment = models.JSONField(default=list)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"غرفة {self.room_number} - {self.ward.name}"


class Bed(models.Model):
    """الأسرّة"""

    STATUS_CHOICES = [
        ("available", "متاح"),
        ("occupied", "مشغول"),
        ("reserved", "محجوز"),
        ("maintenance", "صيانة"),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    bed_number = models.CharField(max_length=50)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="available"
    )
    is_electric = models.BooleanField(default=False)
    last_maintenance = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"سرير {self.bed_number} - غرفة {self.room.room_number}"


class Admission(models.Model):
    """الإدخال للمستشفى"""

    STATUS_CHOICES = [
        ("pending", "قيد الانتظار"),
        ("admitted", "تم الإدخال"),
        ("discharged", "تم الخروج"),
        ("transferred", "تم النقل"),
    ]

    ADMISSION_TYPES = [
        ("emergency", "طوارئ"),
        ("planned", "مخطط"),
        ("transfer", "تحويل"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE)
    admitting_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    admission_type = models.CharField(max_length=20, choices=ADMISSION_TYPES)
    admission_date = models.DateTimeField()
    expected_discharge_date = models.DateField(null=True, blank=True)
    actual_discharge_date = models.DateTimeField(null=True, blank=True)
    diagnosis = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"إدخال {self.patient.user.get_full_name()} - {self.admission_date}"


class Transfer(models.Model):
    """التحويلات"""

    admission = models.ForeignKey(Admission, on_delete=models.CASCADE)
    from_bed = models.ForeignKey(
        Bed, on_delete=models.CASCADE, related_name="transfers_from"
    )
    to_bed = models.ForeignKey(
        Bed, on_delete=models.CASCADE, related_name="transfers_to"
    )
    transfer_date = models.DateTimeField()
    reason = models.TextField()
    authorized_by = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"تحويل {self.admission.patient.user.get_full_name()} - {self.transfer_date}"


class NursingRound(models.Model):
    """جولات التمريض"""

    admission = models.ForeignKey(Admission, on_delete=models.CASCADE)
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    round_time = models.DateTimeField()
    vital_signs = models.JSONField()
    medications_given = models.JSONField(default=list)
    notes = models.TextField(blank=True)
    next_round_time = models.DateTimeField()

    def __str__(self):
        return f"جولة {self.nurse.user.get_full_name()} - {self.round_time}"


class DoctorRound(models.Model):
    """جولات الأطباء"""

    admission = models.ForeignKey(Admission, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    round_time = models.DateTimeField()
    findings = models.TextField()
    instructions = models.TextField()
    medications_prescribed = models.JSONField(default=list)
    next_round_time = models.DateTimeField()

    def __str__(self):
        return f"جولة د.{self.doctor.user.get_full_name()} - {self.round_time}"


class Discharge(models.Model):
    """الخروج من المستشفى"""

    DISCHARGE_TYPES = [
        ("regular", "عادي"),
        ("against_advice", "ضد النصيحة الطبية"),
        ("transfer", "تحويل"),
        ("death", "وفاة"),
    ]

    admission = models.OneToOneField(Admission, on_delete=models.CASCADE)
    discharge_date = models.DateTimeField()
    discharge_type = models.CharField(max_length=20, choices=DISCHARGE_TYPES)
    discharge_diagnosis = models.TextField()
    discharge_summary = models.TextField()
    medications = models.JSONField(default=list)
    follow_up_instructions = models.TextField()
    discharged_by = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"خروج {self.admission.patient.user.get_full_name()} - {self.discharge_date}"


class Equipment(models.Model):
    """المعدات الطبية"""

    EQUIPMENT_TYPES = [
        ("diagnostic", "تشخيصي"),
        ("therapeutic", "علاجي"),
        ("monitoring", "مراقبة"),
        ("life_support", "دعم حياة"),
        ("surgical", "جراحي"),
    ]

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    equipment_type = models.CharField(max_length=20, choices=EQUIPMENT_TYPES)
    model_number = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    manufacturer = models.CharField(max_length=200)
    purchase_date = models.DateField()
    last_maintenance = models.DateField()
    next_maintenance = models.DateField()
    status = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    is_portable = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.serial_number}"


class MaintenanceRecord(models.Model):
    """سجلات الصيانة"""

    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    maintenance_date = models.DateField()
    maintenance_type = models.CharField(max_length=100)
    performed_by = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    findings = models.TextField()
    actions_taken = models.TextField()
    next_maintenance = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"صيانة {self.equipment.name} - {self.maintenance_date}"


class InventoryItem(models.Model):
    """المخزون"""

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=50)
    minimum_quantity = models.PositiveIntegerField()
    supplier = models.CharField(max_length=200)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    last_ordered = models.DateField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} - {self.department.name}"

    class Meta:
        verbose_name_plural = "Inventory Items"
