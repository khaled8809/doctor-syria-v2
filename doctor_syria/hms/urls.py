from django.urls import path

from . import views

app_name = "hms"

urlpatterns = [
    # Dashboard
    path("", views.dashboard, name="dashboard"),
    # Departments
    path("departments/", views.department_list, name="department_list"),
    path("departments/add/", views.department_add, name="department_add"),
    path("departments/<int:pk>/", views.department_detail, name="department_detail"),
    path("departments/<int:pk>/edit/", views.department_edit, name="department_edit"),
    # Wards
    path("wards/", views.ward_list, name="ward_list"),
    path("wards/add/", views.ward_add, name="ward_add"),
    path("wards/<int:pk>/", views.ward_detail, name="ward_detail"),
    path("wards/<int:pk>/edit/", views.ward_edit, name="ward_edit"),
    # Rooms
    path("rooms/", views.room_list, name="room_list"),
    path("rooms/add/", views.room_add, name="room_add"),
    path("rooms/<int:pk>/", views.room_detail, name="room_detail"),
    path("rooms/<int:pk>/edit/", views.room_edit, name="room_edit"),
    # Beds
    path("beds/", views.bed_list, name="bed_list"),
    path("beds/add/", views.bed_add, name="bed_add"),
    path("beds/<int:pk>/", views.bed_detail, name="bed_detail"),
    path("beds/<int:pk>/edit/", views.bed_edit, name="bed_edit"),
    # Admissions
    path("admissions/", views.admission_list, name="admission_list"),
    path("admissions/add/", views.admission_add, name="admission_add"),
    path("admissions/<int:pk>/", views.admission_detail, name="admission_detail"),
    path("admissions/<int:pk>/edit/", views.admission_edit, name="admission_edit"),
    # Transfers
    path("transfers/", views.transfer_list, name="transfer_list"),
    path("transfers/add/", views.transfer_add, name="transfer_add"),
    path("transfers/<int:pk>/", views.transfer_detail, name="transfer_detail"),
    # Nursing Rounds
    path("nursing-rounds/", views.nursing_round_list, name="nursing_round_list"),
    path("nursing-rounds/add/", views.nursing_round_add, name="nursing_round_add"),
    path(
        "nursing-rounds/<int:pk>/",
        views.nursing_round_detail,
        name="nursing_round_detail",
    ),
    # Doctor Rounds
    path("doctor-rounds/", views.doctor_round_list, name="doctor_round_list"),
    path("doctor-rounds/add/", views.doctor_round_add, name="doctor_round_add"),
    path(
        "doctor-rounds/<int:pk>/", views.doctor_round_detail, name="doctor_round_detail"
    ),
    # Discharges
    path("discharges/", views.discharge_list, name="discharge_list"),
    path("discharges/add/", views.discharge_add, name="discharge_add"),
    path("discharges/<int:pk>/", views.discharge_detail, name="discharge_detail"),
    # Equipment
    path("equipment/", views.equipment_list, name="equipment_list"),
    path("equipment/add/", views.equipment_add, name="equipment_add"),
    path("equipment/<int:pk>/", views.equipment_detail, name="equipment_detail"),
    path("equipment/<int:pk>/edit/", views.equipment_edit, name="equipment_edit"),
    # Maintenance
    path("maintenance/", views.maintenance_list, name="maintenance_list"),
    path("maintenance/add/", views.maintenance_add, name="maintenance_add"),
    path("maintenance/<int:pk>/", views.maintenance_detail, name="maintenance_detail"),
    # Inventory
    path("inventory/", views.inventory_list, name="inventory_list"),
    path("inventory/add/", views.inventory_add, name="inventory_add"),
    path("inventory/<int:pk>/", views.inventory_detail, name="inventory_detail"),
    path("inventory/<int:pk>/edit/", views.inventory_edit, name="inventory_edit"),
    # Reports
    path("reports/occupancy/", views.occupancy_report, name="occupancy_report"),
    path("reports/admissions/", views.admissions_report, name="admissions_report"),
    path("reports/discharges/", views.discharges_report, name="discharges_report"),
    path("reports/equipment/", views.equipment_report, name="equipment_report"),
    path("reports/inventory/", views.inventory_report, name="inventory_report"),
    # API Endpoints
    path(
        "api/bed-availability/", views.bed_availability_api, name="bed_availability_api"
    ),
    path(
        "api/department-stats/", views.department_stats_api, name="department_stats_api"
    ),
    path(
        "api/inventory-alerts/", views.inventory_alerts_api, name="inventory_alerts_api"
    ),
]
