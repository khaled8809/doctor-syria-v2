from django.urls import path
from . import views

app_name = 'resource_management'

urlpatterns = [
    path('', views.ResourceListView.as_view(), name='resource_list'),
    path('equipment/', views.MedicalEquipmentListView.as_view(), name='equipment_list'),
    path('operating-rooms/', views.OperatingRoomListView.as_view(), name='operating_room_list'),
    path('beds/', views.BedManagementListView.as_view(), name='bed_list'),
    path('beds/<int:pk>/assign/', views.BedAssignmentView.as_view(), name='bed_assign'),
]
