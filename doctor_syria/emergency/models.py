from django.contrib.gis.db import models as gis_models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from accounts.models import Ambulance, Doctor, Hospital, Patient


class EmergencyCenter(models.Model):
    """مركز الطوارئ"""

    hospital = models.OneToOneField(Hospital, on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField()
    current_occupancy = models.PositiveIntegerField(default=0)
    trauma_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    location = gis_models.PointField()
    is_active = models.BooleanField(default=True)
    specialties_available = models.JSONField(default=list)
    equipment_status = models.JSONField(default=dict)

    def __str__(self):
        return f"طوارئ {self.hospital.name}"

    class Meta:
        verbose_name_plural = "Emergency Centers"


class EmergencyRequest(models.Model):
    """طلب طوارئ"""

    PRIORITY_LEVELS = [
        ("low", "منخفض"),
        ("medium", "متوسط"),
        ("high", "عالي"),
        ("critical", "حرج"),
    ]

    STATUS_CHOICES = [
        ("pending", "قيد الانتظار"),
        ("dispatched", "تم إرسال سيارة إسعاف"),
        ("in_progress", "قيد التنفيذ"),
        ("completed", "مكتمل"),
        ("cancelled", "ملغي"),
    ]

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, null=True, blank=True
    )
    caller_name = models.CharField(max_length=200)
    caller_phone = models.CharField(max_length=20)
    location = gis_models.PointField()
    address_details = models.TextField()
    symptoms = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    assigned_center = models.ForeignKey(
        EmergencyCenter, on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"طلب طوارئ {self.id} - {self.caller_name}"


class AmbulanceDispatch(models.Model):
    """إرسال سيارة إسعاف"""

    STATUS_CHOICES = [
        ("assigned", "تم التعيين"),
        ("en_route", "في الطريق"),
        ("arrived", "وصلت"),
        ("returning", "في طريق العودة"),
        ("completed", "مكتملة"),
        ("cancelled", "ملغية"),
    ]

    emergency_request = models.ForeignKey(EmergencyRequest, on_delete=models.CASCADE)
    ambulance = models.ForeignKey(Ambulance, on_delete=models.CASCADE)
    paramedic_team = models.ManyToManyField("accounts.User")
    dispatch_time = models.DateTimeField(auto_now_add=True)
    arrival_time = models.DateTimeField(null=True, blank=True)
    pickup_time = models.DateTimeField(null=True, blank=True)
    hospital_arrival_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="assigned")
    current_location = gis_models.PointField(null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"إرسال سيارة إسعاف {self.ambulance.number} لطلب {self.emergency_request.id}"


class EmergencyAssessment(models.Model):
    """تقييم حالة الطوارئ"""

    CONSCIOUSNESS_LEVELS = [
        ("alert", "متيقظ"),
        ("verbal", "يستجيب للكلام"),
        ("pain", "يستجيب للألم"),
        ("unresponsive", "غير مستجيب"),
    ]

    dispatch = models.OneToOneField(AmbulanceDispatch, on_delete=models.CASCADE)
    vital_signs = models.JSONField(default=dict)
    consciousness_level = models.CharField(max_length=20, choices=CONSCIOUSNESS_LEVELS)
    chief_complaint = models.TextField()
    assessment_notes = models.TextField()
    treatment_given = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"تقييم طوارئ - {self.dispatch.emergency_request.id}"


class EmergencyProtocol(models.Model):
    """بروتوكولات الطوارئ"""

    name = models.CharField(max_length=200)
    condition = models.CharField(max_length=200)
    steps = models.JSONField()
    medications = models.JSONField(default=list)
    equipment_needed = models.JSONField(default=list)
    notes = models.TextField(blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"بروتوكول {self.name}"


class EmergencyTeam(models.Model):
    """فريق الطوارئ"""

    ROLE_CHOICES = [
        ("doctor", "طبيب"),
        ("nurse", "ممرض"),
        ("paramedic", "مسعف"),
        ("technician", "فني"),
    ]

    center = models.ForeignKey(EmergencyCenter, on_delete=models.CASCADE)
    staff_member = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    shift_start = models.DateTimeField()
    shift_end = models.DateTimeField()
    is_on_duty = models.BooleanField(default=False)
    specialization = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.get_role_display()} - {self.staff_member.get_full_name()}"


class EmergencyBed(models.Model):
    """أسرّة الطوارئ"""

    STATUS_CHOICES = [
        ("available", "متاح"),
        ("occupied", "مشغول"),
        ("reserved", "محجوز"),
        ("maintenance", "صيانة"),
    ]

    center = models.ForeignKey(EmergencyCenter, on_delete=models.CASCADE)
    bed_number = models.CharField(max_length=50)
    bed_type = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="available"
    )
    current_patient = models.ForeignKey(
        Patient, on_delete=models.SET_NULL, null=True, blank=True
    )
    equipment = models.JSONField(default=list)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"سرير {self.bed_number} - {self.center.hospital.name}"


class EmergencyNotification(models.Model):
    """إشعارات الطوارئ"""

    NOTIFICATION_TYPES = [
        ("new_request", "طلب جديد"),
        ("status_update", "تحديث الحالة"),
        ("team_alert", "تنبيه الفريق"),
        ("capacity_alert", "تنبيه السعة"),
        ("critical_patient", "مريض حرج"),
    ]

    center = models.ForeignKey(EmergencyCenter, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    recipients = models.ManyToManyField("accounts.User")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.get_type_display()} - {self.created_at}"
