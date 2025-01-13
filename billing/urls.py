from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"invoices", views.InvoiceViewSet)
router.register(r"payments", views.PaymentViewSet)
router.register(r"insurance-providers", views.InsuranceProviderViewSet)
router.register(r"insurance-claims", views.InsuranceClaimViewSet)

app_name = "billing"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("api/", include(router.urls)),
    path("webhook/stripe/", views.StripeWebhookView.as_view(), name="stripe-webhook"),
    path("webhook/fatura/", views.FaturaWebhookView.as_view(), name="fatura-webhook"),
    path("payment/<int:payment_id>/", views.payment_form, name="payment-form"),
]
