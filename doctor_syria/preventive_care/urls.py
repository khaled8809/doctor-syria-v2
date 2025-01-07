from django.urls import path
from . import views

app_name = 'preventive_care'

urlpatterns = [
    path('', views.PreventiveCareHomeView.as_view(), name='home'),
    path('checkups/', views.PreventiveCheckupListView.as_view(), name='checkup_list'),
    path('checkups/create/', views.PreventiveCheckupCreateView.as_view(), name='checkup_create'),
    path('vaccinations/', views.VaccinationListView.as_view(), name='vaccination_list'),
    path('vaccinations/create/', views.VaccinationCreateView.as_view(), name='vaccination_create'),
    path('health-tips/', views.HealthTipListView.as_view(), name='health_tip_list'),
]
