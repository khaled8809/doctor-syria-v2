"""
أدوات تطبيق الإشعارات
"""

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Notification


def send_notification(user, title, message, notification_type="info"):
    """إرسال إشعار للمستخدم"""
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type,
    )

    # إرسال بريد إلكتروني إذا كان مفعل
    if settings.NOTIFICATION_SETTINGS.get("EMAIL_NOTIFICATIONS", False):
        context = {
            "user": user,
            "notification": notification,
            "site_name": settings.SITE_NAME,
        }
        html_message = render_to_string("notifications/email/notification.html", context)
        send_mail(
            subject=title,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
        )

    return notification
