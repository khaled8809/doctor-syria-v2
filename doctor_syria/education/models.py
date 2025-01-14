from django.db import models
from django.utils.text import slugify

from accounts.models import Doctor, User


class Course(models.Model):
    """الدورات التعليمية"""

    LEVEL_CHOICES = [
        ("beginner", "مبتدئ"),
        ("intermediate", "متوسط"),
        ("advanced", "متقدم"),
    ]

    STATUS_CHOICES = [
        ("draft", "مسودة"),
        ("published", "منشور"),
        ("archived", "مؤرشف"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    instructor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to="courses/")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    duration = models.DurationField(help_text="المدة الإجمالية للدورة")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_free = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    students = models.ManyToManyField(User, through="Enrollment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Module(models.Model):
    """وحدات الدورة"""

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    """الدروس"""

    CONTENT_TYPES = [
        ("video", "فيديو"),
        ("article", "مقال"),
        ("quiz", "اختبار"),
        ("assignment", "واجب"),
    ]

    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    content = models.TextField()
    video_url = models.URLField(blank=True)
    duration = models.DurationField(null=True, blank=True)
    order = models.PositiveIntegerField()
    is_free_preview = models.BooleanField(default=False)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Quiz(models.Model):
    """الاختبارات"""

    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE)
    passing_score = models.PositiveIntegerField(default=70)
    time_limit = models.DurationField(null=True, blank=True)
    attempts_allowed = models.PositiveIntegerField(default=3)

    def __str__(self):
        return f"اختبار {self.lesson.title}"


class Question(models.Model):
    """أسئلة الاختبار"""

    QUESTION_TYPES = [
        ("multiple_choice", "اختيار من متعدد"),
        ("true_false", "صح وخطأ"),
        ("short_answer", "إجابة قصيرة"),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    text = models.TextField()
    points = models.PositiveIntegerField(default=1)
    explanation = models.TextField(blank=True)

    def __str__(self):
        return self.text[:50]


class Answer(models.Model):
    """إجابات الأسئلة"""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    explanation = models.TextField(blank=True)

    def __str__(self):
        return self.text


class Enrollment(models.Model):
    """تسجيل الطلاب"""

    STATUS_CHOICES = [
        ("active", "نشط"),
        ("completed", "مكتمل"),
        ("dropped", "منسحب"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    progress = models.PositiveIntegerField(default=0)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ["user", "course"]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.course.title}"


class Progress(models.Model):
    """تقدم الطالب"""

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_spent = models.DurationField(default=0)

    class Meta:
        unique_together = ["enrollment", "lesson"]

    def __str__(self):
        return f"{self.enrollment.user.get_full_name()} - {self.lesson.title}"


class Certificate(models.Model):
    """الشهادات"""

    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE)
    certificate_number = models.CharField(max_length=100, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="certificates/")

    def __str__(self):
        return f"شهادة {self.enrollment.user.get_full_name()} - {self.enrollment.course.title}"


class HealthGuide(models.Model):
    """الأدلة الإرشادية الصحية"""

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    category = models.CharField(max_length=100)
    author = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    file = models.FileField(upload_to="guides/", null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
