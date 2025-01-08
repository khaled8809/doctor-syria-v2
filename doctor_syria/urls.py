from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Doctor Syria API",
        default_version='v1',
        description="نظام إدارة المستشفيات والعيادات الطبية",
        terms_of_service="https://www.doctor-syria.com/terms/",
        contact=openapi.Contact(email="contact@doctor-syria.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # الصفحة الرئيسية
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    
    # لوحة التحكم
    path('admin/', admin.site.urls),
    
    # توثيق API
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # تطبيقات النظام
    path('api/', include('saas.api_urls')),
    path('appointments/', include('appointments.urls')),
    path('doctor/', include('doctor.urls')),
    path('clinics/', include('clinics.urls')),
    path('pharmacy/', include('medical_store.urls')),
    path('commerce/', include('commerce.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
