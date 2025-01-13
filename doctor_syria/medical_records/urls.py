from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AllergyViewSet,
    AppointmentViewSet,
    MedicalRecordViewSet,
    PrescriptionViewSet,
    VaccinationViewSet,
)

router = DefaultRouter()
router.register(r"medical-records", MedicalRecordViewSet)
router.register(r"appointments", AppointmentViewSet)
router.register(r"prescriptions", PrescriptionViewSet)
router.register(r"allergies", AllergyViewSet)
router.register(r"vaccinations", VaccinationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
