from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from medical_records.models import MedicalRecord

from accounts.models import Doctor, Hospital, Nurse, Patient


class OperatingRoom(models.Model):
    """غرف العمليات"""

    ROOM_TYPES = [
        ("general", "عامة"),
        ("cardiac", "قلب"),
        ("orthopedic", "عظام"),
        ("neurosurgery", "جراحة أعصاب"),
        ("ophthalmic", "عيون"),
        ("hybrid", "هجينة"),
    ]

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=50)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    floor = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    equipment = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    maintenance_schedule = models.JSONField(default=dict)
    last_maintenance = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"غرفة {self.room_number} - {self.get_room_type_display()}"


class Surgery(models.Model):
    """العمليات الجراحية"""

    SURGERY_TYPES = [
        ("elective", "اختيارية"),
        ("urgent", "عاجلة"),
        ("emergency", "طارئة"),
    ]

    STATUS_CHOICES = [
        ("scheduled", "مجدولة"),
        ("in_progress", "قيد التنفيذ"),
        ("completed", "مكتملة"),
        ("cancelled", "ملغية"),
        ("postponed", "مؤجلة"),
    ]

    ANESTHESIA_TYPES = [
        ("local", "موضعي"),
        ("regional", "ناحي"),
        ("general", "عام"),
        ("sedation", "تهدئة"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    operating_room = models.ForeignKey(OperatingRoom, on_delete=models.CASCADE)
    primary_surgeon = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="primary_surgeries"
    )
    assistant_surgeons = models.ManyToManyField(
        Doctor, related_name="assisted_surgeries", blank=True
    )
    anesthesiologist = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="anesthesia_surgeries"
    )
    surgery_type = models.CharField(max_length=20, choices=SURGERY_TYPES)
    procedure_name = models.CharField(max_length=200)
    description = models.TextField()
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    estimated_duration = models.DurationField()
    actual_start_time = models.DateTimeField(null=True, blank=True)
    actual_end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="scheduled"
    )
    anesthesia_type = models.CharField(max_length=20, choices=ANESTHESIA_TYPES)
    pre_op_diagnosis = models.TextField()
    post_op_diagnosis = models.TextField(blank=True)
    complications = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.procedure_name} - {self.patient.user.get_full_name()}"

    class Meta:
        verbose_name_plural = "Surgeries"


class SurgicalTeam(models.Model):
    """الفريق الجراحي"""

    ROLE_CHOICES = [
        ("scrub_nurse", "ممرض معقم"),
        ("circulating_nurse", "ممرض دوار"),
        ("surgical_tech", "فني جراحة"),
        ("perfusionist", "فني قلب رئة"),
        ("other", "أخرى"),
    ]

    surgery = models.ForeignKey(Surgery, on_delete=models.CASCADE)
    staff_member = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_role_display()} - {self.staff_member.get_full_name()}"


class SurgicalEquipment(models.Model):
    """المعدات الجراحية"""

    surgery = models.ForeignKey(Surgery, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    sterilization_date = models.DateField()
    batch_number = models.CharField(max_length=100)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.surgery}"


class SurgicalProcedure(models.Model):
    """إجراءات العملية"""

    surgery = models.ForeignKey(Surgery, on_delete=models.CASCADE)
    step_number = models.PositiveIntegerField()
    description = models.TextField()
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    performed_by = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"خطوة {self.step_number} - {self.surgery}"

    class Meta:
        ordering = ["step_number"]


class SurgicalNote(models.Model):
    """ملاحظات العملية"""

    NOTE_TYPES = [
        ("pre_op", "قبل العملية"),
        ("intra_op", "أثناء العملية"),
        ("post_op", "بعد العملية"),
    ]

    surgery = models.ForeignKey(Surgery, on_delete=models.CASCADE)
    note_type = models.CharField(max_length=20, choices=NOTE_TYPES)
    content = models.TextField()
    created_by = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_note_type_display()} - {self.surgery}"


class PostOpCare(models.Model):
    """الرعاية ما بعد العملية"""

    surgery = models.OneToOneField(Surgery, on_delete=models.CASCADE)
    recovery_room = models.CharField(max_length=50)
    admission_time = models.DateTimeField()
    discharge_time = models.DateTimeField(null=True, blank=True)
    vital_signs = models.JSONField(default=list)
    pain_level = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)], null=True
    )
    medications = models.JSONField(default=list)
    complications = models.TextField(blank=True)
    instructions = models.TextField()

    def __str__(self):
        return f"رعاية ما بعد العملية - {self.surgery}"


class SurgicalConsent(models.Model):
    """الموافقة على العملية"""

    surgery = models.OneToOneField(Surgery, on_delete=models.CASCADE)
    patient_signature = models.ImageField(upload_to="consent_signatures/")
    guardian_signature = models.ImageField(
        upload_to="consent_signatures/", null=True, blank=True
    )
    witness_signature = models.ImageField(upload_to="consent_signatures/")
    signed_at = models.DateTimeField()
    is_valid = models.BooleanField(default=True)
    scanned_document = models.FileField(upload_to="consent_documents/", null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"موافقة على العملية - {self.surgery}"
