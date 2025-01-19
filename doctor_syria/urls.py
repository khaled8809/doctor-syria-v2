"""
URL configuration for doctor_syria project.
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from core import views  # إضافة استيراد views

schema_view = get_schema_view(
    openapi.Info(
        title="Doctor Syria API",
        default_version="v1",
        description="API documentation for Doctor Syria platform",
        terms_of_service="https://www.doctor-syria.com/terms/",
        contact=openapi.Contact(email="contact@doctor-syria.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

api_patterns = [
    # API Documentation
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # Core APIs
    path("auth/", include("accounts.urls")),
    path("core/", include("core.urls")),
    path("utils/", include("utils.urls")),
    # Medical APIs
    path("doctors/", include("doctors.urls")),
    path("clinics/", include("clinics.urls")),
    path("appointments/", include("appointments.urls")),
    path("medical-records/", include("medical_records.urls")),
    path("pharmacy/", include("pharmacy.urls")),
    path("laboratory/", include("laboratory.urls")),
    # Business APIs
    # path("billing/", include("billing.urls")),  # معطل مؤقتاً
    # AI & Analytics APIs
    path("ai-diagnosis/", include("ai_diagnosis.urls")),
    path("analytics/", include("analytics.urls")),
    # path("monitoring/", include("monitoring.urls")),  # معطل مؤقتاً
    path("notifications/", include("notifications.urls")),
]

urlpatterns = i18n_patterns(
    # Admin Interface
    path("admin/", admin.site.urls),
    # API URLs
    path("api/v1/", include(api_patterns)),
    # Frontend URLs
    # path("", include("frontend.urls")),  # معطل مؤقتاً
    # Legal pages
    path(
        "legal/",
        include(
            [
                path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
                path("terms/", views.terms, name="terms"),
            ]
        ),
    ),
    # Help and Support
    path(
        "help/",
        include(
            [
                path("", views.help_home, name="help_home"),
                path("support/", views.support, name="support"),
                path("faq/", views.faq, name="faq"),
            ]
        ),
    ),
    # Settings
    path(
        "settings/",
        include(
            [
                path("general/", views.general_settings, name="general_settings"),
            ]
        ),
    ),
    # Health Check
    path("health/", include("health_check.urls")),
    # Debug Toolbar
    path("__debug__/", include("debug_toolbar.urls")),
    # Prometheus Metrics
    path("metrics/", include("django_prometheus.urls")),
    prefix_default_language=False,
)

# Error pages
handler404 = "core.views.error_404"
handler500 = "core.views.error_500"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
