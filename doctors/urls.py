from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('search/', views.search_doctors, name='search'),
    path('doctor/<int:doctor_id>/', views.doctor_profile, name='doctor_profile'),
    path('blog/', views.blog_list, name='blog_list'),
]
