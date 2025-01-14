import logging
from datetime import datetime, timedelta

import psutil
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.db import connection
from django.db.models import Count
from medical_records.models import MedicalRecord

from accounts.models import User
from appointments.models import Appointment

logger = logging.getLogger(__name__)


class SystemMonitor:
    """نظام مراقبة أداء التطبيق"""

    def __init__(self):
        self.metrics = {}
        self.alerts = []

    def collect_system_metrics(self):
        """جمع مقاييس النظام"""
        try:
            self.metrics.update(
                {
                    "cpu_usage": psutil.cpu_percent(interval=1),
                    "memory_usage": psutil.virtual_memory().percent,
                    "disk_usage": psutil.disk_usage("/").percent,
                }
            )
        except Exception as e:
            logger.error(f"Error collecting system metrics: {str(e)}")

    def collect_database_metrics(self):
        """جمع مقاييس قاعدة البيانات"""
        try:
            with connection.cursor() as cursor:
                # عدد الاتصالات النشطة
                cursor.execute("SELECT count(*) FROM pg_stat_activity")
                active_connections = cursor.fetchone()[0]

                # حجم قاعدة البيانات
                cursor.execute(
                    """
                    SELECT pg_size_pretty(pg_database_size(current_database()))
                """
                )
                db_size = cursor.fetchone()[0]

                self.metrics.update(
                    {
                        "db_connections": active_connections,
                        "db_size": db_size,
                    }
                )
        except Exception as e:
            logger.error(f"Error collecting database metrics: {str(e)}")

    def collect_application_metrics(self):
        """جمع مقاييس التطبيق"""
        try:
            now = datetime.now()
            hour_ago = now - timedelta(hours=1)

            self.metrics.update(
                {
                    "active_users": User.objects.filter(
                        last_login__gte=hour_ago
                    ).count(),
                    "total_appointments_today": Appointment.objects.filter(
                        date__date=now.date()
                    ).count(),
                    "pending_medical_records": MedicalRecord.objects.filter(
                        status="pending"
                    ).count(),
                }
            )
        except Exception as e:
            logger.error(f"Error collecting application metrics: {str(e)}")

    def check_thresholds(self):
        """فحص تجاوز العتبات"""
        thresholds = {
            "cpu_usage": 80,
            "memory_usage": 85,
            "disk_usage": 90,
            "db_connections": 100,
        }

        for metric, value in self.metrics.items():
            if metric in thresholds and value > thresholds[metric]:
                self.alerts.append(
                    {
                        "level": "critical",
                        "message": f"{metric} is too high: {value}%",
                        "timestamp": datetime.now(),
                    }
                )

    def send_alerts(self):
        """إرسال التنبيهات"""
        if not self.alerts:
            return

        critical_alerts = [
            alert for alert in self.alerts if alert["level"] == "critical"
        ]
        if critical_alerts:
            message = "\n".join(
                [
                    f"{alert['timestamp']}: {alert['message']}"
                    for alert in critical_alerts
                ]
            )

            try:
                send_mail(
                    subject="Critical System Alerts",
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=settings.ADMIN_EMAILS,
                    fail_silently=False,
                )
            except Exception as e:
                logger.error(f"Error sending alert email: {str(e)}")

        # تخزين التنبيهات في Redis للعرض في لوحة التحكم
        cache.set("system_alerts", self.alerts, timeout=3600)

    def monitor(self):
        """تشغيل المراقبة الكاملة"""
        self.collect_system_metrics()
        self.collect_database_metrics()
        self.collect_application_metrics()
        self.check_thresholds()
        self.send_alerts()

        # تخزين المقاييس في Redis
        cache.set("system_metrics", self.metrics, timeout=300)  # 5 دقائق

        return {"metrics": self.metrics, "alerts": self.alerts}
