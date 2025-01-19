from django.urls import path
from rest_framework import routers

from . import views

app_name = "resource_management"

# API Router
router = routers.DefaultRouter()
router.register(r'equipment', views.MedicalEquipmentViewSet)
router.register(r'operating-rooms', views.OperatingRoomViewSet)
router.register(r'beds', views.BedManagementViewSet)
router.register(r'staff', views.StaffManagementViewSet)
router.register(r'supplies', views.MedicalSuppliesViewSet)

urlpatterns = [
    # Dashboard
    path("", views.ResourceListView.as_view(), name="resource_list"),
    path("dashboard/", views.ResourceDashboardView.as_view(), name="dashboard"),
    path("dashboard/analytics/", views.ResourceAnalyticsView.as_view(), name="analytics"),
    
    # Equipment Management
    path("equipment/", views.MedicalEquipmentListView.as_view(), name="equipment_list"),
    path("equipment/add/", views.MedicalEquipmentCreateView.as_view(), name="equipment_add"),
    path("equipment/<int:pk>/", views.MedicalEquipmentDetailView.as_view(), name="equipment_detail"),
    path("equipment/maintenance/", views.EquipmentMaintenanceView.as_view(), name="equipment_maintenance"),
    path("equipment/calibration/", views.EquipmentCalibrationView.as_view(), name="equipment_calibration"),
    
    # Operating Room Management
    path("operating-rooms/", views.OperatingRoomListView.as_view(), name="operating_room_list"),
    path("operating-rooms/schedule/", views.OperatingRoomScheduleView.as_view(), name="operating_room_schedule"),
    path("operating-rooms/<int:pk>/", views.OperatingRoomDetailView.as_view(), name="operating_room_detail"),
    path("operating-rooms/maintenance/", views.ORMaintenanceView.as_view(), name="or_maintenance"),
    
    # Bed Management
    path("beds/", views.BedManagementListView.as_view(), name="bed_list"),
    path("beds/<int:pk>/", views.BedDetailView.as_view(), name="bed_detail"),
    path("beds/<int:pk>/assign/", views.BedAssignmentView.as_view(), name="bed_assign"),
    path("beds/occupancy/", views.BedOccupancyView.as_view(), name="bed_occupancy"),
    path("beds/transfers/", views.BedTransferView.as_view(), name="bed_transfers"),
    
    # Staff Management
    path("staff/", views.StaffManagementView.as_view(), name="staff_management"),
    path("staff/schedule/", views.StaffScheduleView.as_view(), name="staff_schedule"),
    path("staff/assignments/", views.StaffAssignmentView.as_view(), name="staff_assignments"),
    path("staff/availability/", views.StaffAvailabilityView.as_view(), name="staff_availability"),
    
    # Supply Management
    path("supplies/", views.MedicalSuppliesView.as_view(), name="supplies"),
    path("supplies/inventory/", views.SupplyInventoryView.as_view(), name="supply_inventory"),
    path("supplies/orders/", views.SupplyOrderView.as_view(), name="supply_orders"),
    path("supplies/tracking/", views.SupplyTrackingView.as_view(), name="supply_tracking"),
    
    # Resource Allocation
    path("allocation/", views.ResourceAllocationView.as_view(), name="resource_allocation"),
    path("allocation/requests/", views.AllocationRequestView.as_view(), name="allocation_requests"),
    path("allocation/priorities/", views.AllocationPriorityView.as_view(), name="allocation_priorities"),
    
    # Reports
    path("reports/utilization/", views.UtilizationReportView.as_view(), name="utilization_report"),
    path("reports/efficiency/", views.EfficiencyReportView.as_view(), name="efficiency_report"),
    path("reports/costs/", views.CostAnalysisView.as_view(), name="cost_analysis"),
    
    # Settings
    path("settings/", views.ResourceSettingsView.as_view(), name="settings"),
    path("settings/notifications/", views.NotificationSettingsView.as_view(), name="notification_settings"),
    path("settings/thresholds/", views.ThresholdSettingsView.as_view(), name="threshold_settings"),
]

urlpatterns += router.urls
