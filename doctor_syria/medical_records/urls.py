from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MedicalRecordViewSet, AppointmentViewSet,
    PrescriptionViewSet, AllergyViewSet,
    VaccinationViewSet
)

router = DefaultRouter()
router.register(r'medical-records', MedicalRecordViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'allergies', AllergyViewSet)
router.register(r'vaccinations', VaccinationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
