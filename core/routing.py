"""
WebSocket routing configuration for doctor_syria project.
"""

from django.urls import re_path

from core.consumers import (
    AppointmentStatusConsumer,
    ChatConsumer,
    LiveDashboardConsumer,
    NotificationConsumer,
)

websocket_urlpatterns = [
    re_path(r"ws/notifications/$", NotificationConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/appointments/status/$", AppointmentStatusConsumer.as_asgi()),
    re_path(r"ws/dashboard/live/$", LiveDashboardConsumer.as_asgi()),
]
