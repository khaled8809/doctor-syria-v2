"""
خدمات نظام الإشعارات
"""

import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from core.utils import send_sms  # افتراضي - يجب تنفيذه

from .models import Notification, NotificationPreference


class NotificationService:
    """خدمة إدارة الإشعارات"""

    @staticmethod
    def create_notification(
        recipient,
        notification_type,
        title,
        message,
        priority="normal",
        related_object=None,
        metadata=None,
    ):
        """إنشاء إشعار جديد"""
        notification = Notification.objects.create(
            recipient=recipient,
            notification_type=notification_type,
            title=title,
            message=message,
            priority=priority,
            metadata=metadata or {},
        )

        if related_object:
            notification.content_type = ContentType.objects.get_for_model(
                related_object
            )
            notification.object_id = related_object.id
            notification.save()

        # إرسال الإشعار عبر القنوات المناسبة
        NotificationService.send_notification(notification)
        return notification

    @staticmethod
    def send_notification(notification):
        """إرسال الإشعار عبر القنوات المختلفة"""
        preferences = NotificationPreference.objects.get_or_create(
            user=notification.recipient
        )[0]

        # التحقق من ساعات الهدوء
        if NotificationService.is_quiet_hours(preferences):
            return

        # إرسال إشعار فوري عبر WebSocket
        if preferences.push_notifications:
            NotificationService.send_websocket_notification(notification)

        # إرسال بريد إلكتروني
        if preferences.email_notifications:
            NotificationService.send_email_notification(notification)

        # إرسال رسالة نصية
        if preferences.sms_notifications and notification.priority in [
            "high",
            "urgent",
        ]:
            NotificationService.send_sms_notification(notification)

    @staticmethod
    def send_websocket_notification(notification):
        """إرسال إشعار عبر WebSocket"""
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{notification.recipient.id}",
            {
                "type": "notification.message",
                "message": {
                    "id": notification.id,
                    "type": notification.notification_type,
                    "title": notification.title,
                    "message": notification.message,
                    "priority": notification.priority,
                    "created_at": notification.created_at.isoformat(),
                },
            },
        )

    @staticmethod
    def send_email_notification(notification):
        """إرسال إشعار عبر البريد الإلكتروني"""
        context = {"notification": notification, "recipient": notification.recipient}

        html_message = render_to_string(
            "notifications/email_notification.html", context
        )

        send_mail(
            subject=notification.title,
            message=notification.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[notification.recipient.email],
            html_message=html_message,
        )

    @staticmethod
    def send_sms_notification(notification):
        """إرسال إشعار عبر الرسائل النصية"""
        message = f"{notification.title}\n{notification.message}"
        send_sms(phone_number=notification.recipient.phone_number, message=message)

    @staticmethod
    def is_quiet_hours(preferences):
        """التحقق مما إذا كان الوقت الحالي ضمن ساعات الهدوء"""
        if not preferences.quiet_hours_start or not preferences.quiet_hours_end:
            return False

        current_time = timezone.localtime().time()
        if preferences.quiet_hours_start <= preferences.quiet_hours_end:
            return (
                preferences.quiet_hours_start
                <= current_time
                <= preferences.quiet_hours_end
            )
        else:  # عندما تمتد ساعات الهدوء عبر منتصف الليل
            return (
                current_time >= preferences.quiet_hours_start
                or current_time <= preferences.quiet_hours_end
            )

    @staticmethod
    def mark_as_read(notification_id, user):
        """تحديد إشعار كمقروء"""
        try:
            notification = Notification.objects.get(id=notification_id, recipient=user)
            notification.mark_as_read()
            return True
        except Notification.DoesNotExist:
            return False

    @staticmethod
    def mark_all_as_read(user):
        """تحديد جميع إشعارات المستخدم كمقروءة"""
        Notification.objects.filter(recipient=user, is_read=False).update(
            is_read=True, read_at=timezone.now()
        )
