from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from accounts.models import Doctor, Hospital, Patient, User


class QualityStandard(models.Model):
    """معايير الجودة"""

    STANDARD_TYPES = [
        ("clinical", "سريري"),
        ("operational", "تشغيلي"),
        ("safety", "سلامة"),
        ("patient_care", "رعاية المرضى"),
        ("documentation", "توثيق"),
    ]

    name = models.CharField(max_length=200)
    standard_type = models.CharField(max_length=20, choices=STANDARD_TYPES)
    description = models.TextField()
    criteria = models.JSONField()
    target_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_standard_type_display()}"


class Audit(models.Model):
    """التدقيق"""

    STATUS_CHOICES = [
        ("planned", "مخطط"),
        ("in_progress", "قيد التنفيذ"),
        ("completed", "مكتمل"),
        ("reviewed", "تمت المراجعة"),
    ]

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    standards = models.ManyToManyField(QualityStandard)
    audit_date = models.DateField()
    auditor = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")
    findings = models.JSONField(default=dict)
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True,
    )
    recommendations = models.TextField(blank=True)
    next_audit_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"تدقيق {self.hospital.name} - {self.audit_date}"


class Incident(models.Model):
    """الحوادث"""

    SEVERITY_LEVELS = [
        ("low", "منخفض"),
        ("medium", "متوسط"),
        ("high", "عالي"),
        ("critical", "حرج"),
    ]

    STATUS_CHOICES = [
        ("reported", "تم الإبلاغ"),
        ("investigating", "قيد التحقيق"),
        ("resolved", "تم الحل"),
        ("closed", "مغلق"),
    ]

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    incident_date = models.DateTimeField()
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="reported")
    affected_patients = models.ManyToManyField(Patient, blank=True)
    immediate_action = models.TextField()
    root_cause = models.TextField(blank=True)
    corrective_action = models.TextField(blank=True)
    preventive_measures = models.TextField(blank=True)
    resolution_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"حادث {self.get_severity_display()} - {self.incident_date}"


class Category(models.Model):
    """فئات الأسئلة"""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    order = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Question(models.Model):
    """الأسئلة"""

    STATUS_CHOICES = [
        ("pending", "قيد المراجعة"),
        ("published", "منشور"),
        ("closed", "مغلق"),
    ]

    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.CharField(max_length=500, blank=True, help_text="Comma separated tags")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    is_anonymous = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Answer(models.Model):
    """الإجابات"""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    is_best = models.BooleanField(default=False)
    upvotes = models.ManyToManyField(User, related_name="upvoted_answers", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_best", "-created_at"]

    def __str__(self):
        return f"إجابة على {self.question.title}"

    def upvotes_count(self):
        return self.upvotes.count()


class Comment(models.Model):
    """التعليقات"""

    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"تعليق من {self.user.get_full_name()}"


class QuestionBookmark(models.Model):
    """إشارات مرجعية للأسئلة"""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("question", "user")

    def __str__(self):
        return f"إشارة مرجعية لـ {self.question.title}"


class ImprovementPlan(models.Model):
    """خطط التحسين"""

    STATUS_CHOICES = [
        ("planned", "مخطط"),
        ("in_progress", "قيد التنفيذ"),
        ("completed", "مكتمل"),
        ("on_hold", "معلق"),
    ]

    PRIORITY_LEVELS = [
        ("low", "منخفض"),
        ("medium", "متوسط"),
        ("high", "عالي"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    responsible_person = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")
    start_date = models.DateField()
    target_completion_date = models.DateField()
    actual_completion_date = models.DateField(null=True, blank=True)
    success_criteria = models.TextField()
    resources_needed = models.TextField()
    progress_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"خطة تحسين: {self.title}"
