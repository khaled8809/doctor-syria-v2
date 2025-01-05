from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.AppointmentListCreateView.as_view(), name='appointment_list'),
    path('<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('prescriptions/', views.PrescriptionListCreateView.as_view(), name='prescription_list'),
    path('prescriptions/<int:pk>/', views.PrescriptionDetailView.as_view(), name='prescription_detail'),
    path('medical-records/', views.MedicalRecordListCreateView.as_view(), name='medical_record_list'),
    path('medical-records/<int:pk>/', views.MedicalRecordDetailView.as_view(), name='medical_record_detail'),
]
