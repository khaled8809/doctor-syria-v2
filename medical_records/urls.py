"""
URLs for the medical records app
"""

from django.urls import path
from . import views

app_name = 'medical_records'

urlpatterns = [
    path('', views.RecordListView.as_view(), name='list'),
    path('create/', views.RecordCreateView.as_view(), name='create'),
    path('<int:pk>/', views.RecordDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.RecordUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.RecordDeleteView.as_view(), name='delete'),
]
