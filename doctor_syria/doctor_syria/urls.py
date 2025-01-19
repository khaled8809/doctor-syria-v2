"""
URL configuration for doctor_syria project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.documentation import include_docs_urls

api_v1_patterns = [
    path("accounts/", include("accounts.urls")),
    path("appointments/", include("appointments.urls")),
    path("pharmacy/", include("pharmacy.urls")),
    path("laboratory/", include("laboratory.urls")),
    path("preventive-care/", include("preventive_care.urls")),
    path("ai-diagnosis/", include("ai_diagnosis.urls")),
    path("resource-management/", include("resource_management.urls")),
    path("medical-education/", include("medical_education.urls")),
    path("decision-support/", include("decision_support.urls")),
]

urlpatterns = [
    # Admin interface
    path("admin/", admin.site.urls),
    
    # API endpoints
    path("api/v1/", include((api_v1_patterns, "api_v1"))),
    path("api/docs/", include_docs_urls(title="Doctor Syria API Documentation")),
    
    # Web interface
    path("", include("core.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
