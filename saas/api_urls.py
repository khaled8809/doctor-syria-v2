from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import api_views

router = DefaultRouter()
router.register(r'reports', api_views.ReportViewSet)
router.register(r'medical-devices', api_views.MedicalDeviceViewSet)
router.register(r'device-readings', api_views.DeviceReadingViewSet)
router.register(r'ai-models', api_views.AIModelViewSet)
router.register(r'ai-predictions', api_views.AIPredictionViewSet)
router.register(r'resources', api_views.ResourceViewSet)
router.register(r'resource-schedules', api_views.ResourceScheduleViewSet)
router.register(r'chat-rooms', api_views.ChatRoomViewSet)
router.register(r'messages', api_views.MessageViewSet)
router.register(r'video-calls', api_views.VideoCallViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
