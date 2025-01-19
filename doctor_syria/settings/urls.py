from django.urls import include, path
from rest_framework import routers

from . import views

app_name = "settings"

# API Router
router = routers.DefaultRouter()

# إعدادات النظام
router.register(r'system', views.SystemSettingViewSet, basename='system')
router.register(r'working-hours', views.WorkingHourViewSet, basename='working-hour')
router.register(r'holidays', views.HolidayViewSet, basename='holiday')

# القوالب والإشعارات
router.register(r'email-templates', views.EmailTemplateViewSet, basename='email-template')
router.register(r'sms-templates', views.SMSTemplateViewSet, basename='sms-template')
router.register(r'notification-settings', views.NotificationSettingViewSet, basename='notification-setting')

# التخصيص والتفضيلات
router.register(r'currencies', views.CurrencyViewSet, basename='currency')
router.register(r'languages', views.LanguageViewSet, basename='language')
router.register(r'themes', views.ThemeViewSet, basename='theme')

# النسخ الاحتياطي
router.register(r'backup-schedules', views.BackupScheduleViewSet, basename='backup-schedule')

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
]
