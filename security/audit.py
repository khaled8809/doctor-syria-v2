from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone


class SecurityAudit(models.Model):
    """نموذج لتسجيل الأحداث الأمنية"""

    SEVERITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
        ("CRITICAL", "Critical"),
    ]

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="security_audits",
    )
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True)
    severity = models.CharField(max_length=8, choices=SEVERITY_CHOICES, default="LOW")
    details = models.JSONField(default=dict)

    # للربط مع أي نموذج في النظام
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["timestamp"]),
            models.Index(fields=["severity"]),
        ]

    def __str__(self):
        return f"{self.timestamp} - {self.action} by {self.user}"
