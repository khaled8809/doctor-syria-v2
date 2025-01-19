"""
Utility functions for the notifications application.
"""
from django.utils import timezone

from .models import Notification


def send_notification(user, title, message, notification_type='info', related_object=None):
    """
    Send a notification to a user.

    Args:
        user: The user to send the notification to
        title: The title of the notification
        message: The message content of the notification
        notification_type: The type of notification (info, success, warning, error)
        related_object: Optional related object for the notification

    Returns:
        The created notification object
    """
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type,
        content_object=related_object,
        created_at=timezone.now()
    )
    return notification
