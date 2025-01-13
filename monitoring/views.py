from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .alert_manager import AlertManager
from .system_monitor import SystemMonitor


class MonitoringViewSet(viewsets.ViewSet):
    """واجهة برمجة التطبيقات للمراقبة"""

    permission_classes = [permissions.IsAdminUser]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.system_monitor = SystemMonitor()
        self.alert_manager = AlertManager()

    @cache_page(60)  # تخزين مؤقت لمدة دقيقة
    @action(detail=False, methods=["get"])
    def system_status(self, request):
        """الحصول على حالة النظام الحالية"""
        status_data = self.system_monitor.monitor()
        return Response(status_data)

    @action(detail=False, methods=["get"])
    def recent_alerts(self, request):
        """الحصول على التنبيهات الأخيرة"""
        alerts = cache.get("system_alerts", [])
        return Response(alerts)

    @action(detail=False, methods=["get"])
    def performance_metrics(self, request):
        """الحصول على مقاييس الأداء"""
        metrics = cache.get("system_metrics", {})
        return Response(metrics)

    @action(detail=False, methods=["post"])
    def test_alert(self, request):
        """اختبار نظام التنبيهات"""
        message = request.data.get("message", "Test alert")
        severity = request.data.get("severity", "medium")

        success = self.alert_manager.send_alert(
            message=message, severity=severity, users=[request.user], send_email=True
        )

        return Response(
            {
                "success": success,
                "message": (
                    "Alert sent successfully" if success else "Failed to send alert"
                ),
            }
        )


@method_decorator(staff_member_required, name="dispatch")
class DashboardView(TemplateView):
    """عرض لوحة التحكم"""

    template_name = "monitoring/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "لوحة المراقبة"
        return context
