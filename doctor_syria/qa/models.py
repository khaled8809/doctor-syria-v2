from django.db import models
from django.utils.text import slugify
from accounts.models import User, Doctor, Patient


class Category(models.Model):
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
    STATUS_CHOICES = (
        ("pending", "قيد المراجعة"),
        ("published", "منشور"),
        ("closed", "مغلق"),
    )

    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.CharField(
        max_length=500, blank=True, help_text="Comma separated tags"
    )
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

    @property
    def answers_count(self):
        return self.answer_set.count()

    @property
    def best_answer(self):
        return self.answer_set.filter(is_best=True).first()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    is_best = models.BooleanField(default=False)
    upvotes = models.ManyToManyField(User, related_name="upvoted_answers", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_best", "-upvotes__count", "-created_at"]

    def __str__(self):
        return f"إجابة على {self.question.title}"

    @property
    def upvotes_count(self):
        return self.upvotes.count()


class Comment(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"تعليق من {self.user.get_full_name()}"


class QuestionBookmark(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("question", "user")

    def __str__(self):
        return f"{self.user.get_full_name()} حفظ {self.question.title}"
