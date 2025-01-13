from django.urls import path

from . import views

app_name = "saas"

urlpatterns = [
    path("register/", views.register_tenant, name="register_tenant"),
    path("plans/", views.subscription_plans, name="subscription_plans"),
    path("dashboard/", views.tenant_dashboard, name="tenant_dashboard"),
]
