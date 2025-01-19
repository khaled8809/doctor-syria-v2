from django.urls import include, path
from rest_framework import routers

from . import views

app_name = "profiles"

# API Router
router = routers.DefaultRouter()
router.register(r'profiles', views.ProfileViewSet, basename='profile')
router.register(r'education', views.EducationViewSet, basename='education')
router.register(r'experience', views.ExperienceViewSet, basename='experience')
router.register(r'certifications', views.CertificationViewSet, basename='certification')
router.register(r'awards', views.AwardViewSet, basename='award')
router.register(r'publications', views.PublicationViewSet, basename='publication')
router.register(r'contacts', views.ContactViewSet, basename='contact')
router.register(r'emergency-contacts', views.EmergencyContactViewSet, basename='emergency-contact')
router.register(r'insurance', views.InsuranceViewSet, basename='insurance')

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
]
