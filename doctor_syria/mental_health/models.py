from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from accounts.models import Doctor, Patient


class MentalHealthProfile(models.Model):
    """الملف النفسي"""

    MARITAL_STATUS = [
        ("single", "أعزب/عزباء"),
        ("married", "متزوج/ة"),
        ("divorced", "مطلق/ة"),
        ("widowed", "أرمل/ة"),
    ]

    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    primary_therapist = models.ForeignKey(
        Doctor, on_delete=models.SET_NULL, null=True, related_name="primary_patients"
    )
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS)
    occupation = models.CharField(max_length=200)
    living_situation = models.TextField()
    family_history = models.TextField()
    previous_treatments = models.TextField(blank=True)
    current_medications = models.JSONField(default=list)
    risk_factors = models.JSONField(default=list)
    support_system = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"الملف النفسي - {self.patient.user.get_full_name()}"


class TherapySession(models.Model):
    """جلسات العلاج النفسي"""

    SESSION_TYPES = [
        ("individual", "فردية"),
        ("group", "جماعية"),
        ("family", "عائلية"),
        ("couple", "زوجية"),
    ]

    SESSION_MODES = [
        ("in_person", "حضوري"),
        ("video", "فيديو"),
        ("phone", "هاتف"),
        ("chat", "محادثة"),
    ]

    STATUS_CHOICES = [
        ("scheduled", "مجدولة"),
        ("in_progress", "جارية"),
        ("completed", "مكتملة"),
        ("cancelled", "ملغية"),
        ("no_show", "لم يحضر"),
    ]

    profile = models.ForeignKey(MentalHealthProfile, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES)
    session_mode = models.CharField(max_length=20, choices=SESSION_MODES)
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="scheduled"
    )
    session_notes = models.TextField(blank=True)
    homework_assigned = models.TextField(blank=True)
    next_session_goals = models.TextField(blank=True)

    def __str__(self):
        return f"جلسة {self.get_session_type_display()} - {self.profile.patient.user.get_full_name()}"


class MoodTracker(models.Model):
    """متتبع المزاج"""

    MOOD_CHOICES = [
        (1, "سيء جداً"),
        (2, "سيء"),
        (3, "محايد"),
        (4, "جيد"),
        (5, "جيد جداً"),
    ]

    profile = models.ForeignKey(MentalHealthProfile, on_delete=models.CASCADE)
    mood_level = models.IntegerField(choices=MOOD_CHOICES)
    energy_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    sleep_hours = models.FloatField()
    anxiety_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    stress_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    activities = models.JSONField(default=list)
    notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField()

    def __str__(self):
        return f"تتبع المزاج - {self.profile.patient.user.get_full_name()} - {self.recorded_at}"


class Assessment(models.Model):
    """التقييمات النفسية"""

    ASSESSMENT_TYPES = [
        ("initial", "تقييم أولي"),
        ("progress", "تقييم التقدم"),
        ("discharge", "تقييم الخروج"),
        ("crisis", "تقييم أزمة"),
    ]

    profile = models.ForeignKey(MentalHealthProfile, on_delete=models.CASCADE)
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPES)
    therapist = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    symptoms = models.JSONField()
    diagnosis = models.JSONField()
    risk_assessment = models.TextField()
    recommendations = models.TextField()
    next_steps = models.TextField()

    def __str__(self):
        return f"{self.get_assessment_type_display()} - {self.profile.patient.user.get_full_name()}"


class Treatment(models.Model):
    """خطط العلاج"""

    STATUS_CHOICES = [
        ("active", "نشطة"),
        ("completed", "مكتملة"),
        ("discontinued", "متوقفة"),
    ]

    profile = models.ForeignKey(MentalHealthProfile, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    goals = models.JSONField()
    interventions = models.JSONField()
    progress_notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    medications = models.JSONField(default=list)
    review_date = models.DateField()

    def __str__(self):
        return f"خطة علاج - {self.profile.patient.user.get_full_name()}"


class SupportGroup(models.Model):
    """مجموعات الدعم"""

    name = models.CharField(max_length=200)
    description = models.TextField()
    facilitator = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    max_participants = models.PositiveIntegerField()
    meeting_schedule = models.JSONField()
    is_active = models.BooleanField(default=True)
    focus_area = models.CharField(max_length=200)
    rules = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class GroupMembership(models.Model):
    """عضوية المجموعات"""

    STATUS_CHOICES = [
        ("active", "نشط"),
        ("inactive", "غير نشط"),
        ("suspended", "موقوف"),
    ]

    group = models.ForeignKey(SupportGroup, on_delete=models.CASCADE)
    profile = models.ForeignKey(MentalHealthProfile, on_delete=models.CASCADE)
    join_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    attendance_record = models.JSONField(default=list)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.profile.patient.user.get_full_name()} - {self.group.name}"


class Crisis(models.Model):
    """حالات الأزمات"""

    SEVERITY_LEVELS = [
        ("mild", "خفيفة"),
        ("moderate", "متوسطة"),
        ("severe", "شديدة"),
        ("critical", "حرجة"),
    ]

    profile = models.ForeignKey(MentalHealthProfile, on_delete=models.CASCADE)
    reported_at = models.DateTimeField()
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    description = models.TextField()
    immediate_action = models.TextField()
    follow_up_required = models.BooleanField(default=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)

    def __str__(self):
        return (
            f"أزمة - {self.profile.patient.user.get_full_name()} - {self.reported_at}"
        )

    class Meta:
        verbose_name_plural = "Crises"


class Worksheet(models.Model):
    """أوراق العمل العلاجية"""

    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.JSONField()
    instructions = models.TextField()
    target_symptoms = models.JSONField(default=list)
    recommended_frequency = models.CharField(max_length=100)
    created_by = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
