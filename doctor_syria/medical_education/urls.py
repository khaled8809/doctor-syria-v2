from django.urls import path
from . import views

app_name = 'medical_education'

urlpatterns = [
    path('courses/', views.CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('simulations/', views.VirtualSimulationListView.as_view(), name='simulation-list'),
    path('library/', views.MedicalLibraryListView.as_view(), name='library-list'),
]
