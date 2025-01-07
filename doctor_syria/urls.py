from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # الصفحة الرئيسية تحول إلى لوحة التحكم
    path('', RedirectView.as_view(url='/accounts/dashboard/', permanent=False), name='home'),
    
    # تطبيقات النظام
    path('accounts/', include('accounts.urls')),
    # path('appointments/', include('appointments.urls')),
    # path('medical_records/', include('medical_records.urls')),
]

# إضافة مسارات الوسائط في وضع التطوير
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
