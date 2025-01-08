from django.conf import settings
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from .models import Tenant

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_site = get_current_site(request)
        domain_parts = current_site.domain.split('.')
        
        # Check if this is a subdomain request
        if len(domain_parts) > 2:
            subdomain = domain_parts[0]
            try:
                tenant = Tenant.objects.get(subdomain=subdomain, is_active=True)
                request.tenant = tenant
            except Tenant.DoesNotExist:
                return redirect(settings.MAIN_SITE_URL)
        else:
            request.tenant = None
            
        response = self.get_response(request)
        return response
