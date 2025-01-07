from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('doctors/', views.DoctorListView.as_view(), name='doctor_list'),
    path('doctors/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor_detail'),
    path('pharmacies/', views.PharmacyListView.as_view(), name='pharmacy_list'),
    path('pharmacies/<int:pk>/', views.PharmacyDetailView.as_view(), name='pharmacy_detail'),
    path('laboratories/', views.LaboratoryListView.as_view(), name='laboratory_list'),
    path('laboratories/<int:pk>/', views.LaboratoryDetailView.as_view(), name='laboratory_detail'),
]
