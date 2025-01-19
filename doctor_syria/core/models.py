from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from accounts.models import Doctor, Patient, User


class TimestampMixin(models.Model):
    """
    Mixin لإضافة حقول التوقيت
    """

    created_at = models.DateTimeField(_("تاريخ الإنشاء"), default=timezone.now)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    """
    Mixin للحذف الناعم
    """

    is_deleted = models.BooleanField(_("محذوف"), default=False)
    deleted_at = models.DateTimeField(_("تاريخ الحذف"), null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        """
        تنفيذ الحذف الناعم
        """
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """
        استعادة العنصر المحذوف
        """
        self.is_deleted = False
        self.deleted_at = None
        self.save()


class AuditMixin(models.Model):
    """
    Mixin لتتبع التغييرات
    """

    created_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
        verbose_name=_("تم الإنشاء بواسطة"),
    )
    updated_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
        verbose_name=_("تم التحديث بواسطة"),
    )
    deleted_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_deleted",
        verbose_name=_("تم الحذف بواسطة"),
    )

    class Meta:
        abstract = True


class Article(TimestampMixin, AuditMixin, SoftDeleteMixin, models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=500)
    image = models.ImageField(upload_to="articles/", null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-published_at"]


class Review(TimestampMixin, AuditMixin, SoftDeleteMixin, models.Model):
    RATING_CHOICES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
