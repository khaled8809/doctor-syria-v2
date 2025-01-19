from django.urls import path
from rest_framework import routers

from . import views

app_name = "billing"

# API Router
router = routers.DefaultRouter()
router.register(r'invoices', views.InvoiceViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'price-lists', views.PriceListViewSet)
router.register(r'insurance-claims', views.InsuranceClaimViewSet)

urlpatterns = [
    # Invoice Management
    path("invoices/", views.InvoiceListCreateView.as_view(), name="invoice-list"),
    path("invoices/<int:pk>/", views.InvoiceDetailView.as_view(), name="invoice-detail"),
    path("invoices/<int:pk>/pdf/", views.InvoicePDFView.as_view(), name="invoice-pdf"),
    path("invoices/<int:pk>/email/", views.InvoiceEmailView.as_view(), name="invoice-email"),
    path("invoices/pending/", views.PendingInvoicesView.as_view(), name="pending-invoices"),
    
    # Payment Management
    path("payments/", views.PaymentListCreateView.as_view(), name="payment-list"),
    path("payments/<int:pk>/", views.PaymentDetailView.as_view(), name="payment-detail"),
    path("payments/process/", views.ProcessPaymentView.as_view(), name="process-payment"),
    path("payments/refund/<int:pk>/", views.RefundPaymentView.as_view(), name="refund-payment"),
    
    # Price Lists and Services
    path("price-lists/", views.PriceListView.as_view(), name="price-list"),
    path("price-lists/services/", views.ServicePricesView.as_view(), name="service-prices"),
    path("price-lists/packages/", views.PackagePricesView.as_view(), name="package-prices"),
    path("price-lists/discounts/", views.DiscountListView.as_view(), name="discounts"),
    
    # Insurance Claims
    path("insurance/claims/", views.InsuranceClaimListView.as_view(), name="insurance-claims"),
    path("insurance/claims/<int:pk>/", views.InsuranceClaimDetailView.as_view(), name="claim-detail"),
    path("insurance/claims/submit/", views.SubmitClaimView.as_view(), name="submit-claim"),
    path("insurance/verification/", views.InsuranceVerificationView.as_view(), name="insurance-verification"),
    
    # Reports and Analytics
    path("reports/revenue/", views.RevenueReportView.as_view(), name="revenue-report"),
    path("reports/transactions/", views.TransactionReportView.as_view(), name="transaction-report"),
    path("reports/insurance/", views.InsuranceReportView.as_view(), name="insurance-report"),
    path("analytics/", views.BillingAnalyticsView.as_view(), name="billing-analytics"),
]

urlpatterns += router.urls
