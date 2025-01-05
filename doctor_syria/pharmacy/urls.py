from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('', views.PharmacyListView.as_view(), name='pharmacy_list'),
    path('<int:pk>/', views.PharmacyDetailView.as_view(), name='pharmacy_detail'),
    path('medicines/', views.MedicineListCreateView.as_view(), name='medicine_list'),
    path('medicines/<int:pk>/', views.MedicineDetailView.as_view(), name='medicine_detail'),
    path('inventory/', views.PharmacyInventoryListView.as_view(), name='inventory_list'),
    path('inventory/<int:pk>/', views.PharmacyInventoryDetailView.as_view(), name='inventory_detail'),
    path('orders/', views.MedicineOrderListCreateView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.MedicineOrderDetailView.as_view(), name='order_detail'),
    path('categories/', views.MedicineCategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.MedicineCategoryDetailView.as_view(), name='category_detail'),
]
