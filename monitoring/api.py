"""
واجهات برمجة التطبيقات للمراقبة
"""

from datetime import timedelta

from django.db.models import Avg, Count
from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ErrorLog, PerformanceLog, SystemMetric
from .serializers import (
    ErrorLogSerializer,
    PerformanceLogSerializer,
    SystemMetricSerializer,
)


class MonitoringViewSet(viewsets.ReadOnlyModelViewSet):
    """
    واجهة برمجة التطبيقات للوصول إلى بيانات المراقبة
    """

    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=["get"])
    def system_health(self, request):
        """
        الحصول على حالة صحة النظام
        """
        # حساب متوسط استخدام الموارد في آخر ساعة
        last_hour = timezone.now() - timedelta(hours=1)
        metrics = SystemMetric.objects.filter(timestamp__gte=last_hour)

        cpu_usage = metrics.filter(metric_type="cpu").aggregate(Avg("value"))
        memory_usage = metrics.filter(metric_type="memory").aggregate(Avg("value"))
        response_time = metrics.filter(metric_type="response_time").aggregate(
            Avg("value")
        )

        # حساب معدل الأخطاء
        error_rate = (
            ErrorLog.objects.filter(timestamp__gte=last_hour).count() / 3600
        )  # errors per second

        return Response(
            {
                "cpu_usage": cpu_usage["value__avg"],
                "memory_usage": memory_usage["value__avg"],
                "average_response_time": response_time["value__avg"],
                "error_rate": error_rate,
                "status": "healthy" if error_rate < 0.1 else "degraded",
            }
        )

    @action(detail=False, methods=["get"])
    def performance_stats(self, request):
        """
        الحصول على إحصائيات الأداء
        """
        last_day = timezone.now() - timedelta(days=1)
        performance_logs = PerformanceLog.objects.filter(timestamp__gte=last_day)

        # تحليل الأداء حسب نقطة النهاية
        endpoint_stats = performance_logs.values("endpoint").annotate(
            avg_response_time=Avg("response_time"),
            request_count=Count("id"),
            error_count=Count("status_code", filter__gte=400),
        )

        return Response(
            {
                "endpoint_stats": endpoint_stats,
                "total_requests": performance_logs.count(),
                "error_percentage": (
                    (
                        performance_logs.filter(status_code__gte=400).count()
                        / performance_logs.count()
                        * 100
                    )
                    if performance_logs.count() > 0
                    else 0
                ),
            }
        )

    @action(detail=False, methods=["get"])
    def error_summary(self, request):
        """
        ملخص الأخطاء
        """
        last_day = timezone.now() - timedelta(days=1)
        errors = ErrorLog.objects.filter(timestamp__gte=last_day)

        severity_counts = errors.values("severity").annotate(count=Count("id"))
        source_counts = errors.values("source").annotate(count=Count("id"))

        return Response(
            {
                "total_errors": errors.count(),
                "severity_distribution": severity_counts,
                "source_distribution": source_counts,
                "recent_errors": ErrorLogSerializer(
                    errors.order_by("-timestamp")[:10], many=True
                ).data,
            }
        )
