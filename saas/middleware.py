from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

from .models import Tenant
from .services.saas_service import SaaSService


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get domain from request
        domain = request.get_host().split(":")[0]

        # Exclude non-tenant URLs
        if any(url in request.path for url in settings.PUBLIC_URLS):
            return self.get_response(request)

        try:
            # Get tenant for this domain
            tenant = Tenant.objects.get(domain=domain, is_active=True)
            request.tenant = tenant

            # Check subscription status
            if not tenant.subscription.is_active():
                if request.path != reverse("subscription_expired"):
                    return redirect("subscription_expired")

        except Tenant.DoesNotExist:
            if request.path != reverse("tenant_not_found"):
                return redirect("tenant_not_found")

        return self.get_response(request)


class FeatureAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not hasattr(request, "tenant"):
            return self.get_response(request)

        # Get feature code from URL pattern
        feature_code = self.get_feature_code(request.path)
        if feature_code:
            # Check feature access
            if not SaaSService.check_feature_access(request.tenant, feature_code):
                return redirect("feature_not_available")

            # Track feature usage
            SaaSService.track_usage(request.tenant, feature_code)

        return self.get_response(request)

    def get_feature_code(self, path):
        """Map URL paths to feature codes."""
        feature_map = {
            "/doctor/": "doctor_dashboard",
            "/clinics/": "clinic_management",
            "/pharmacy/": "pharmacy_management",
            "/commerce/": "ecommerce",
            "/analytics/": "analytics",
            "/emergency/": "emergency_management",
            "/ambulance/": "ambulance_management",
        }

        for url_path, code in feature_map.items():
            if url_path in path:
                return code

        return None
