"""
URL configuration for the accounts application.
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "accounts"

router = DefaultRouter()
router.register(r"doctors", views.DoctorViewSet, basename="doctor")
router.register(r"patients", views.PatientViewSet, basename="patient")
router.register(r"specializations", views.SpecializationViewSet, basename="specialization")
router.register(r"insurance", views.InsuranceViewSet, basename="insurance")

urlpatterns = [
    path("", include(router.urls)),
]
