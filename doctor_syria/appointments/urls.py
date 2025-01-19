"""
URL configuration for the appointments application.
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "appointments"

router = DefaultRouter()
router.register(r"appointments", views.AppointmentViewSet, basename="appointment")

urlpatterns = [
    path("", include(router.urls)),
]
