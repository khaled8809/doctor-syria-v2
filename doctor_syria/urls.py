from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # الصفحة الرئيسية
    path('', TemplateView.as_view(template_name='landing.html'), name='home'),
    
    # تطبيقات النظام
    path('accounts/', include('accounts.urls')),
    path('appointments/', include('appointments.urls')),
    path('medical_records/', include('medical_records.urls')),
    path('pharmacy/', include('pharmacy.urls')),
    path('laboratory/', include('laboratory.urls')),
]

# إضافة مسارات الوسائط في وضع التطوير
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
