from django.urls import path

from . import views

app_name = "pharmacy"

urlpatterns = [
    # إدارة الأدوية
    path("medicines/", views.MedicineListView.as_view(), name="medicine-list"),
    path(
        "medicines/create/", views.MedicineCreateView.as_view(), name="medicine-create"
    ),
    path(
        "medicines/<int:pk>/",
        views.MedicineDetailView.as_view(),
        name="medicine-detail",
    ),
    path(
        "medicines/<int:pk>/update/",
        views.MedicineUpdateView.as_view(),
        name="medicine-update",
    ),
    path(
        "medicines/<int:pk>/delete/",
        views.MedicineDeleteView.as_view(),
        name="medicine-delete",
    ),
    # إدارة الوصفات الطبية
    path(
        "prescriptions/", views.PrescriptionListView.as_view(), name="prescription-list"
    ),
    path(
        "prescriptions/create/",
        views.PrescriptionCreateView.as_view(),
        name="prescription-create",
    ),
    path(
        "prescriptions/<int:pk>/",
        views.PrescriptionDetailView.as_view(),
        name="prescription-detail",
    ),
    path(
        "prescriptions/<int:pk>/update/",
        views.PrescriptionUpdateView.as_view(),
        name="prescription-update",
    ),
    path(
        "prescriptions/<int:pk>/delete/",
        views.PrescriptionDeleteView.as_view(),
        name="prescription-delete",
    ),
    path(
        "prescriptions/<int:pk>/dispense/",
        views.PrescriptionDispenseView.as_view(),
        name="prescription-dispense",
    ),
    # إدارة المخزون
    path("inventory/", views.InventoryListView.as_view(), name="inventory-list"),
    path("inventory/add/", views.InventoryAddView.as_view(), name="inventory-add"),
    path(
        "inventory/report/",
        views.InventoryReportView.as_view(),
        name="inventory-report",
    ),
    path("inventory/low-stock/", views.LowStockView.as_view(), name="low-stock"),
]
