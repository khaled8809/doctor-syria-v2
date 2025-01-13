"""
URLs for the API
"""

from django.urls import include, path

urlpatterns = [
    path("accounts/", include("accounts.api.urls")),
    path("appointments/", include("appointments.api.urls")),
    path("medical-records/", include("medical_records.api.urls")),
    path("notifications/", include("notifications.api.urls")),
    path("analytics/", include("analytics.api.urls")),
]
