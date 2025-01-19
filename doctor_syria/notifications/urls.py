"""
URLs configuration for the notifications application.

This module defines all URL patterns for the notifications app, including:
- Real-time notification management
- Notification preferences and templates
- WebSocket and SSE connections
- Push notifications and device management
"""
from django.urls import include, path

from core.api.routers import create_router
from . import views

app_name = "notifications"

# Create router with app-specific settings
router = create_router(app_name)

# الإشعارات والتفضيلات
router.register(
    r'notifications',
    views.NotificationViewSet,
    basename='notification'
)
router.register(
    r'preferences',
    views.NotificationPreferenceViewSet,
    basename='preference'
)

# القوالب والقنوات
router.register(
    r'templates',
    views.NotificationTemplateViewSet,
    basename='template'
)
router.register(
    r'channels',
    views.NotificationChannelViewSet,
    basename='channel'
)

# الأجهزة والاتصال
router.register(
    r'devices',
    views.DeviceTokenViewSet,
    basename='device'
)

# Define URL patterns
urlpatterns = [
    # API URLs - يشمل جميع نقاط النهاية للـ API
    path('api/v1/', include((router.urls, app_name), namespace='api')),
    
    # Real-time URLs - روابط الاتصال المباشر
    path('realtime/', include([
        path('ws/connect/', views.WebSocketConnectionView.as_view(), name='ws-connect'),
        path('sse/connect/', views.SSEConnectionView.as_view(), name='sse-connect'),
        path('push/subscribe/', views.PushSubscriptionView.as_view(), name='push-subscribe'),
    ])),
    
    # Notification Management - إدارة الإشعارات
    path('notifications/', include([
        path('', views.NotificationListView.as_view(), name='notification-list'),
        path('unread/', views.UnreadNotificationsView.as_view(), name='unread'),
        path('mark-all-read/', views.MarkAllReadView.as_view(), name='mark-all-read'),
        path('<int:pk>/', include([
            path('', views.NotificationDetailView.as_view(), name='notification-detail'),
            path('mark-read/', views.MarkNotificationReadView.as_view(), name='mark-read'),
        ])),
    ])),
    
    # Preferences Management - إدارة التفضيلات
    path('preferences/', include([
        path('', views.PreferencesView.as_view(), name='preferences'),
        path('update/', views.UpdatePreferencesView.as_view(), name='update-preferences'),
        path('channels/', views.NotificationChannelsView.as_view(), name='channels'),
    ])),
    
    # Templates Management - إدارة القوالب
    path('templates/', include([
        path('', views.NotificationTemplateListView.as_view(), name='template-list'),
        path('create/', views.NotificationTemplateCreateView.as_view(), name='template-create'),
        path('<int:pk>/', include([
            path('', views.NotificationTemplateDetailView.as_view(), name='template-detail'),
            path('preview/', views.TemplatePreviewView.as_view(), name='template-preview'),
        ])),
    ])),
    
    # Bulk Operations - العمليات الجماعية
    path('bulk/', include([
        path('send/', views.BulkNotificationView.as_view(), name='bulk-send'),
        path('delete/', views.BulkDeleteView.as_view(), name='bulk-delete'),
    ])),
    
    # Analytics and Reports - التحليلات والتقارير
    path('analytics/', include([
        path('', views.NotificationAnalyticsView.as_view(), name='analytics'),
        path('reports/', views.NotificationReportsView.as_view(), name='reports'),
        path('stats/', views.NotificationStatsView.as_view(), name='stats'),
    ])),
]
