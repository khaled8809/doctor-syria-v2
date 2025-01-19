from django.urls import include, path
from rest_framework import routers

from . import views

app_name = "users"

# API Router
router = routers.DefaultRouter()

# المستخدمين والأدوار
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'roles', views.RoleViewSet, basename='role')
router.register(r'groups', views.GroupViewSet, basename='group')

# الأقسام والتخصصات
router.register(r'departments', views.DepartmentViewSet, basename='department')
router.register(r'specialties', views.SpecialtyViewSet, basename='specialty')

# الموظفين
router.register(r'staff', views.StaffViewSet, basename='staff')

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
]
