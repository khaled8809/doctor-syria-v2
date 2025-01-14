import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from ..models import Notification, NotificationPreference


class NotificationService:
    @staticmethod
    def create_notification(
        recipient,
        title,
        message,
        notification_type,
        priority="MEDIUM",
        related_object=None,
        scheduled_for=None,
    ):
        """Create a new notification."""
        try:
            # Check user preferences
            preferences = NotificationPreference.objects.get_or_create(user=recipient)[
                0
            ]
            if not preferences.can_send_notification(notification_type):
                return None

            # Create notification object
            notification = Notification.objects.create(
                recipient=recipient,
                title=title,
                message=message,
                notification_type=notification_type,
                priority=priority,
                scheduled_for=scheduled_for,
            )

            # Add related object if provided
            if related_object:
                notification.related_object_type = f"{related_object._meta.app_label}.{related_object._meta.model_name}"
                notification.related_object_id = related_object.id
                notification.save()

            # Send real-time notification
            NotificationService.send_realtime_notification(notification)

            # Send email if enabled
            if preferences.email_notifications:
                NotificationService.send_email_notification(notification)

            # Send push notification if enabled
            if preferences.push_notifications:
                NotificationService.send_push_notification(notification)

            # Send SMS if enabled and urgent
            if preferences.sms_notifications and priority == "URGENT":
                NotificationService.send_sms_notification(notification)

            return notification

        except Exception as e:
            print(f"Error creating notification: {str(e)}")
            return None

    @staticmethod
    def send_realtime_notification(notification):
        """Send real-time notification using WebSocket."""
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"notifications_{notification.recipient.id}",
                {
                    "type": "notification.message",
                    "message": {
                        "id": notification.id,
                        "title": notification.title,
                        "message": notification.message,
                        "type": notification.notification_type,
                        "priority": notification.priority,
                        "created_at": notification.created_at.isoformat(),
                    },
                },
            )
        except Exception as e:
            print(f"Error sending real-time notification: {str(e)}")

    @staticmethod
    def send_email_notification(notification):
        """Send email notification."""
        try:
            context = {
                "notification": notification,
                "recipient": notification.recipient,
            }

            html_message = render_to_string("notifications/email.html", context)
            plain_message = render_to_string("notifications/email.txt", context)

            send_mail(
                subject=notification.title,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[notification.recipient.email],
                html_message=html_message,
            )
        except Exception as e:
            print(f"Error sending email notification: {str(e)}")

    @staticmethod
    def send_push_notification(notification):
        """Send push notification using Firebase Cloud Messaging."""
        try:
            # Implementation depends on your push notification service
            pass
        except Exception as e:
            print(f"Error sending push notification: {str(e)}")

    @staticmethod
    def send_sms_notification(notification):
        """Send SMS notification using Twilio or similar service."""
        try:
            # Implementation depends on your SMS service
            pass
        except Exception as e:
            print(f"Error sending SMS notification: {str(e)}")

    @staticmethod
    def create_appointment_reminder(appointment):
        """Create reminder notification for an appointment."""
        notification = NotificationService.create_notification(
            recipient=appointment.patient.user,
            title="Appointment Reminder",
            message=f"You have an appointment scheduled for {appointment.start_time.strftime('%B %d, %Y at %I:%M %p')}",
            notification_type="APPOINTMENT",
            priority="MEDIUM",
            related_object=appointment,
            scheduled_for=appointment.start_time - timezone.timedelta(hours=24),
        )
        return notification

    @staticmethod
    def create_maintenance_alert(device):
        """Create maintenance alert notification."""
        notification = NotificationService.create_notification(
            recipient=device.assigned_technician,
            title="Maintenance Required",
            message=f"Maintenance is due for {device.name}",
            notification_type="MAINTENANCE",
            priority="HIGH",
            related_object=device,
            scheduled_for=device.next_maintenance - timezone.timedelta(days=3),
        )
        return notification

    @staticmethod
    def create_task_notification(task):
        """Create task assignment notification."""
        notification = NotificationService.create_notification(
            recipient=task.assigned_to,
            title="New Task Assigned",
            message=f"You have been assigned a new task: {task.title}",
            notification_type="TASK",
            priority="MEDIUM",
            related_object=task,
        )
        return notification

    @staticmethod
    def create_report_notification(report):
        """Create report generation notification."""
        notification = NotificationService.create_notification(
            recipient=report.created_by,
            title="Report Generated",
            message=f"Your report '{report.title}' has been generated",
            notification_type="REPORT",
            priority="LOW",
            related_object=report,
        )
        return notification

    @staticmethod
    def create_ai_prediction_notification(prediction):
        """Create AI prediction result notification."""
        notification = NotificationService.create_notification(
            recipient=prediction.requested_by,
            title="AI Prediction Result",
            message=f"New AI prediction result available for {prediction.model_name}",
            notification_type="AI_PREDICTION",
            priority="HIGH",
            related_object=prediction,
        )
        return notification

    @staticmethod
    def get_unread_notifications(user):
        """Get unread notifications for a user."""
        return Notification.objects.filter(
            recipient=user, is_read=False, is_archived=False
        ).order_by("-created_at")

    @staticmethod
    def mark_all_as_read(user):
        """Mark all notifications as read for a user."""
        Notification.objects.filter(recipient=user, is_read=False).update(is_read=True)

    @staticmethod
    def clear_old_notifications(days=30):
        """Archive notifications older than specified days."""
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        Notification.objects.filter(
            created_at__lt=cutoff_date, is_archived=False
        ).update(is_archived=True)
