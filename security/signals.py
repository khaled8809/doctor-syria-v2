from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import SecurityAudit

User = get_user_model()


@receiver(post_save, sender=User)
def log_user_changes(sender, instance, created, **kwargs):
    """تسجيل التغييرات على حسابات المستخدمين"""
    action = "User Created" if created else "User Updated"
    SecurityAudit.objects.create(
        user=instance,
        action=action,
        severity="MEDIUM",
        details={
            "username": instance.username,
            "is_active": instance.is_active,
            "is_staff": instance.is_staff,
        },
    )


@receiver(post_delete, sender=User)
def log_user_deletion(sender, instance, **kwargs):
    """تسجيل حذف حسابات المستخدمين"""
    SecurityAudit.objects.create(
        action="User Deleted",
        severity="HIGH",
        details={
            "username": instance.username,
            "user_id": instance.id,
        },
    )
