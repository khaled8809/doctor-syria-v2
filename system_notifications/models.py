from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    """نموذج الإشعارات"""

    NOTIFICATION_TYPES = [
        ("appointment", _("Appointment")),
        ("medical", _("Medical")),
        ("system", _("System")),
    ]

    PRIORITY_LEVELS = [
        ("low", _("Low")),
        ("medium", _("Medium")),
        ("high", _("High")),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("User"),
    )

    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default="system",
        verbose_name=_("Notification Type"),
    )

    title = models.CharField(max_length=255, verbose_name=_("Title"))

    message = models.TextField(verbose_name=_("Message"))

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_LEVELS,
        default="medium",
        verbose_name=_("Priority"),
    )

    is_read = models.BooleanField(default=False, verbose_name=_("Is Read"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    read_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Read At"))

    related_link = models.URLField(blank=True, verbose_name=_("Related Link"))

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.title}"

    def mark_as_read(self):
        """تحديد الإشعار كمقروء"""
        from django.utils import timezone

        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
