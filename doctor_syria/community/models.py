from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from accounts.models import Doctor, Patient, User


class Group(models.Model):
    """مجموعات الدعم والنقاش"""

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to="groups/", blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name="joined_groups")
    moderators = models.ManyToManyField(User, related_name="moderated_groups")
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("community:group_detail", kwargs={"slug": self.slug})


class Post(models.Model):
    """المنشورات في المجموعات"""

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    content = models.TextField()
    image = models.ImageField(upload_to="posts/", blank=True)
    likes = models.ManyToManyField(User, related_name="liked_posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Event(models.Model):
    """الفعاليات وورش العمل"""

    STATUS_CHOICES = (
        ("upcoming", "قادم"),
        ("ongoing", "جاري"),
        ("completed", "منتهي"),
        ("cancelled", "ملغي"),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to="events/")
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_participants = models.PositiveIntegerField()
    participants = models.ManyToManyField(User, related_name="registered_events")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="upcoming")
    is_online = models.BooleanField(default=False)
    meeting_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class HealthTip(models.Model):
    """النصائح الصحية اليومية"""

    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to="health_tips/", blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    likes = models.ManyToManyField(User, related_name="liked_tips")
    is_featured = models.BooleanField(default=False)
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title


class Story(models.Model):
    """قصص وتجارب المرضى"""

    STATUS_CHOICES = (
        ("pending", "قيد المراجعة"),
        ("approved", "تمت الموافقة"),
        ("rejected", "مرفوض"),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    condition = models.CharField(max_length=100)
    image = models.ImageField(upload_to="stories/", blank=True)
    is_anonymous = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    likes = models.ManyToManyField(User, related_name="liked_stories")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Stories"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    """التعليقات على المنشورات والقصص"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Generic Foreign Key
    content_type = models.ForeignKey(
        "contenttypes.ContentType", on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = models.GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"تعليق من {self.user.get_full_name()}"


class Notification(models.Model):
    """الإشعارات للمستخدمين"""

    NOTIFICATION_TYPES = (
        ("group_invite", "دعوة لمجموعة"),
        ("new_post", "منشور جديد"),
        ("event_reminder", "تذكير بفعالية"),
        ("comment", "تعليق جديد"),
        ("like", "إعجاب"),
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.URLField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.notification_type} لـ {self.recipient.get_full_name()}"
