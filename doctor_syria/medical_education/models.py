from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="courses_teaching"
    )
    students = models.ManyToManyField(User, related_name="courses_enrolled")
    start_date = models.DateField()
    end_date = models.DateField()
    credits = models.IntegerField()

    def __str__(self):
        return self.title


class VirtualSimulation(models.Model):
    title = models.CharField(max_length=200)
    procedure_type = models.CharField(max_length=100)
    difficulty_level = models.CharField(max_length=50)
    vr_content_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.procedure_type}"


class MedicalLibrary(models.Model):
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=50)  # Article, Video, Research Paper
    content_url = models.URLField()
    authors = models.CharField(max_length=200)
    publication_date = models.DateField()
    keywords = models.JSONField()

    def __str__(self):
        return self.title
