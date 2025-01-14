from django.db import models
from django.utils import timezone

from accounts.models import Doctor, Patient


class Consultation(models.Model):
    """الاستشارات الطبية"""

    STATUS_CHOICES = [
        ("pending", "قيد الانتظار"),
        ("active", "جارية"),
        ("completed", "مكتملة"),
        ("cancelled", "ملغية"),
    ]

    TYPE_CHOICES = [
        ("chat", "محادثة نصية"),
        ("video", "مكالمة فيديو"),
        ("voice", "مكالمة صوتية"),
    ]

    URGENCY_CHOICES = [
        ("normal", "عادية"),
        ("urgent", "عاجلة"),
        ("emergency", "طارئة"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    consultation_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default="normal")
    chief_complaint = models.TextField()
    symptoms = models.TextField()
    duration = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    meeting_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"استشارة {self.patient.user.get_full_name()} مع د.{self.doctor.user.get_full_name()}"

    def start_consultation(self):
        self.status = "active"
        self.started_at = timezone.now()
        self.save()

    def end_consultation(self):
        self.status = "completed"
        self.ended_at = timezone.now()
        self.save()


class Message(models.Model):
    """رسائل المحادثة"""

    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    sender = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    content = models.TextField()
    file = models.FileField(upload_to="consultation_files/", null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"رسالة من {self.sender.get_full_name()}"


class Prescription(models.Model):
    """الوصفات الطبية الإلكترونية"""

    STATUS_CHOICES = [
        ("active", "نشطة"),
        ("filled", "صُرفت"),
        ("expired", "منتهية"),
        ("cancelled", "ملغية"),
    ]

    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    valid_until = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"وصفة {self.patient.user.get_full_name()} من د.{self.doctor.user.get_full_name()}"


class PrescriptionItem(models.Model):
    """أدوية الوصفة"""

    FREQUENCY_CHOICES = [
        ("daily", "يومياً"),
        ("twice_daily", "مرتين يومياً"),
        ("three_times", "ثلاث مرات يومياً"),
        ("four_times", "أربع مرات يومياً"),
        ("weekly", "أسبوعياً"),
        ("as_needed", "عند الحاجة"),
    ]

    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    medication_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    duration = models.CharField(max_length=100)
    quantity = models.IntegerField()
    instructions = models.TextField()

    def __str__(self):
        return f"{self.medication_name} - {self.prescription}"


class ConsultationNote(models.Model):
    """ملاحظات الطبيب"""

    consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE)
    subjective = models.TextField(help_text="شكوى المريض")
    objective = models.TextField(help_text="الفحص السريري")
    assessment = models.TextField(help_text="التقييم")
    plan = models.TextField(help_text="خطة العلاج")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ملاحظات استشارة {self.consultation}"


class FollowUp(models.Model):
    """متابعة الحالة"""

    STATUS_CHOICES = [
        ("pending", "قيد الانتظار"),
        ("completed", "مكتملة"),
        ("cancelled", "ملغية"),
    ]

    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    scheduled_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["scheduled_date"]

    def __str__(self):
        return f"متابعة استشارة {self.consultation}"
