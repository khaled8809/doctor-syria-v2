import logging
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


class AlertManager:
    """مدير التنبيهات للنظام"""

    SEVERITY_LEVELS = {"critical": 1, "high": 2, "medium": 3, "low": 4}

    def __init__(self):
        self.channel_layer = get_channel_layer()

    def send_alert(self, message, severity="medium", users=None, send_email=False):
        """
        إرسال تنبيه للمستخدمين

        :param message: نص التنبيه
        :param severity: مستوى الأهمية (critical, high, medium, low)
        :param users: قائمة المستخدمين المستهدفين (None لإرسال للجميع)
        :param send_email: إرسال بريد إلكتروني أيضاً
        """
        try:
            alert_data = {
                "type": "system_alert",
                "message": message,
                "severity": severity,
                "timestamp": datetime.now().isoformat(),
            }

            # إرسال التنبيه عبر WebSocket
            if users:
                for user in users:
                    async_to_sync(self.channel_layer.group_send)(
                        f"user_{user.id}", alert_data
                    )
            else:
                async_to_sync(self.channel_layer.group_send)(
                    "system_alerts", alert_data
                )

            # إرسال بريد إلكتروني إذا كان مطلوباً
            if send_email and users:
                self._send_email_alert(message, severity, users)

            logger.info(f"Alert sent: {message} (Severity: {severity})")
            return True

        except Exception as e:
            logger.error(f"Error sending alert: {str(e)}")
            return False

    def _send_email_alert(self, message, severity, users):
        """إرسال تنبيه عبر البريد الإلكتروني"""
        try:
            subject = f"[{severity.upper()}] System Alert"
            email_message = f"""
            System Alert

            Severity: {severity}
            Time: {datetime.now()}
            Message: {message}

            This is an automated message from the Doctor Syria system.
            """

            recipient_list = [user.email for user in users if user.email]
            if recipient_list:
                send_mail(
                    subject=subject,
                    message=email_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=recipient_list,
                    fail_silently=True,
                )
        except Exception as e:
            logger.error(f"Error sending email alert: {str(e)}")

    def broadcast_system_status(self, status_data):
        """بث حالة النظام لجميع المستخدمين المتصلين"""
        try:
            async_to_sync(self.channel_layer.group_send)(
                "system_status",
                {
                    "type": "system_status_update",
                    "data": status_data,
                    "timestamp": datetime.now().isoformat(),
                },
            )
            return True
        except Exception as e:
            logger.error(f"Error broadcasting system status: {str(e)}")
            return False
