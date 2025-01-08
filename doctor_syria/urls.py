"""
URL configuration for doctor_syria project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Doctor Syria API",
        default_version='v1',
        description="Doctor Syria API documentation",
        terms_of_service="https://www.doctor-syria.com/terms/",
        contact=openapi.Contact(email="contact@doctor-syria.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

api_patterns = [
    # API Documentation
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Core APIs
    path('auth/', include('accounts.urls')),
    path('core/', include('core.urls')),
    path('utils/', include('utils.urls')),
    
    # Medical APIs
    path('doctors/', include('doctor.urls')),
    path('patients/', include('patient_records.urls')),
    path('appointments/', include('appointments.urls')),
    path('medical-store/', include('medical_store.urls')),
    path('pharmacy/', include('pharmacy.urls')),
    path('laboratory/', include('laboratory.urls')),
    path('radiology/', include('radiology.urls')),
    
    # Business APIs
    path('billing/', include('billing.urls')),
    path('commerce/', include('commerce.urls')),
    path('hr/', include('hr.urls')),
    
    # Analytics & Monitoring APIs
    path('analytics/', include('analytics.urls')),
    path('monitoring/', include('monitoring.urls')),
    path('notifications/', include('system_notifications.urls')),
    
    # Infrastructure APIs
    path('saas/', include('saas.urls')),
]

urlpatterns = i18n_patterns(
    # Admin Interface
    path('admin/', admin.site.urls),
    
    # API URLs
    path('api/v1/', include(api_patterns)),
    
    # Frontend URLs
    path('', include('frontend.urls')),
    
    # Health Check
    path('health/', include('health_check.urls')),
    
    # Debug Toolbar
    path('__debug__/', include('debug_toolbar.urls')),
    
    # Prometheus Metrics
    path('metrics/', include('django_prometheus.urls')),
    
    prefix_default_language=False
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
