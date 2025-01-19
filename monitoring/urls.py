from django.urls import path

from . import views

app_name = "monitoring"

urlpatterns = [
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path(
        "api/system-status/",
        views.MonitoringViewSet.as_view({"get": "system_status"}),
        name="system-status",
    ),
    path(
        "api/recent-alerts/",
        views.MonitoringViewSet.as_view({"get": "recent_alerts"}),
        name="recent-alerts",
    ),
    path(
        "api/performance-metrics/",
        views.MonitoringViewSet.as_view({"get": "performance_metrics"}),
        name="performance-metrics",
    ),
    path(
        "api/test-alert/",
        views.MonitoringViewSet.as_view({"post": "test_alert"}),
        name="test-alert",
    ),
]
