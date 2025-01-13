"""
Middleware للمراقبة وتتبع الأداء
"""

import logging
import time

import psutil
from django.db import connection

from .models import PerformanceLog, SystemMetric

logger = logging.getLogger(__name__)


class PerformanceMonitoringMiddleware:
    """
    Middleware لمراقبة أداء النظام وتسجيل الإحصائيات
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # تسجيل وقت بداية الطلب
        start_time = time.time()

        # تسجيل استخدام الموارد قبل معالجة الطلب
        cpu_before = psutil.cpu_percent()
        memory_before = psutil.virtual_memory().percent

        # معالجة الطلب
        response = self.get_response(request)

        # حساب زمن الاستجابة
        response_time = time.time() - start_time

        try:
            # تسجيل معلومات الأداء
            PerformanceLog.objects.create(
                endpoint=request.path,
                method=request.method,
                response_time=response_time,
                status_code=response.status_code,
                user=request.user if request.user.is_authenticated else None,
            )

            # تسجيل مقاييس النظام
            SystemMetric.objects.create(
                metric_type="cpu", value=psutil.cpu_percent() - cpu_before
            )

            SystemMetric.objects.create(
                metric_type="memory",
                value=psutil.virtual_memory().percent - memory_before,
            )

            # تسجيل معدل الطلبات
            SystemMetric.objects.create(
                metric_type="response_time", value=response_time
            )

        except Exception as e:
            logger.error(f"Error in PerformanceMonitoringMiddleware: {str(e)}")

        return response


class DatabaseQueryMonitoringMiddleware:
    """
    Middleware لمراقبة استعلامات قاعدة البيانات
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # تسجيل عدد الاستعلامات قبل معالجة الطلب
        n_queries_before = len(connection.queries)

        response = self.get_response(request)

        # حساب عدد الاستعلامات المنفذة
        n_queries_after = len(connection.queries)
        n_queries = n_queries_after - n_queries_before

        try:
            if n_queries > 10:  # تسجيل تحذير إذا كان عدد الاستعلامات كبيراً
                logger.warning(
                    f"High number of database queries ({n_queries}) "
                    f"for request to {request.path}"
                )
        except Exception as e:
            logger.error(f"Error in DatabaseQueryMonitoringMiddleware: {str(e)}")

        return response
