from django.db import models
from django.utils import timezone
from medical_records.models import VitalSigns

from accounts.models import Doctor, Patient


class VirtualClinic(models.Model):
    """العيادة الافتراضية"""

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    working_hours = models.JSONField(default=dict)  # ساعات العمل لكل يوم
    max_daily_appointments = models.PositiveIntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"عيادة د.{self.doctor.user.get_full_name()}"


class VirtualWaitingRoom(models.Model):
    """غرفة الانتظار الافتراضية"""

    STATUS_CHOICES = [
        ("waiting", "في الانتظار"),
        ("in_consultation", "في الاستشارة"),
        ("completed", "اكتملت"),
        ("cancelled", "ملغية"),
    ]

    clinic = models.ForeignKey(VirtualClinic, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_time = models.DateTimeField()
    check_in_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="waiting")
    estimated_wait_time = models.DurationField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["appointment_time"]

    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.appointment_time}"


class TeleSession(models.Model):
    """جلسة الطب عن بُعد"""

    SESSION_TYPES = [
        ("video", "مكالمة فيديو"),
        ("audio", "مكالمة صوتية"),
        ("chat", "محادثة نصية"),
    ]

    STATUS_CHOICES = [
        ("scheduled", "مجدولة"),
        ("in_progress", "جارية"),
        ("completed", "مكتملة"),
        ("cancelled", "ملغية"),
    ]

    clinic = models.ForeignKey(VirtualClinic, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    session_type = models.CharField(max_length=10, choices=SESSION_TYPES)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="scheduled"
    )
    scheduled_start = models.DateTimeField()
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    meeting_url = models.URLField(blank=True)
    session_key = models.CharField(max_length=100, unique=True)
    recording_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"جلسة {self.get_session_type_display()} مع {self.patient.user.get_full_name()}"

    @property
    def duration(self):
        if self.actual_start and self.actual_end:
            return self.actual_end - self.actual_start
        return None


class RemoteVitalSign(models.Model):
    """قياسات حيوية عن بُعد"""

    session = models.ForeignKey(TeleSession, on_delete=models.CASCADE)
    vital_sign = models.ForeignKey(VitalSigns, on_delete=models.CASCADE)
    device_type = models.CharField(max_length=100)
    device_id = models.CharField(max_length=100)
    measurement_time = models.DateTimeField()
    value = models.JSONField()  # تخزين القيم مع وحداتها
    is_normal = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-measurement_time"]

    def __str__(self):
        return (
            f"قياس {self.vital_sign} للمريض {self.session.patient.user.get_full_name()}"
        )


class MedicalDocument(models.Model):
    """المستندات الطبية"""

    DOCUMENT_TYPES = [
        ("lab_result", "نتيجة تحليل"),
        ("prescription", "وصفة طبية"),
        ("medical_report", "تقرير طبي"),
        ("xray", "صورة أشعة"),
        ("other", "أخرى"),
    ]

    session = models.ForeignKey(TeleSession, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="telemedicine_docs/")
    uploaded_by = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.title}"


class SmartDevice(models.Model):
    """الأجهزة الطبية الذكية"""

    DEVICE_TYPES = [
        ("blood_pressure", "جهاز ضغط الدم"),
        ("glucose_meter", "جهاز قياس السكر"),
        ("heart_monitor", "جهاز مراقبة القلب"),
        ("pulse_oximeter", "جهاز قياس الأكسجين"),
        ("thermometer", "ميزان حرارة"),
        ("other", "أخرى"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    device_name = models.CharField(max_length=100)
    device_id = models.CharField(max_length=100, unique=True)
    manufacturer = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)
    last_sync = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    connection_info = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.get_device_type_display()} - {self.device_name}"


class DeviceReading(models.Model):
    """قراءات الأجهزة الطبية"""

    device = models.ForeignKey(SmartDevice, on_delete=models.CASCADE)
    reading_time = models.DateTimeField()
    reading_value = models.JSONField()
    is_normal = models.BooleanField(default=True)
    synced_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-reading_time"]

    def __str__(self):
        return f"قراءة {self.device.device_name} - {self.reading_time}"


class TeleReport(models.Model):
    """تقارير المتابعة الآلية"""

    session = models.ForeignKey(TeleSession, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)
    report_type = models.CharField(max_length=50)
    content = models.JSONField()
    is_reviewed = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(
        Doctor, on_delete=models.SET_NULL, null=True, blank=True
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"تقرير {self.report_type} - {self.session}"
