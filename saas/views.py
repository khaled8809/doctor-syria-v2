from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Tenant, TenantUser, SubscriptionPlan
from .forms import TenantRegistrationForm

@login_required
def register_tenant(request):
    if request.method == 'POST':
        form = TenantRegistrationForm(request.POST)
        if form.is_valid():
            tenant = form.save()
            TenantUser.objects.create(
                user=request.user,
                tenant=tenant,
                is_tenant_admin=True
            )
            messages.success(request, 'Your organization has been registered successfully!')
            return redirect('tenant_dashboard')
    else:
        form = TenantRegistrationForm()
    
    return render(request, 'saas/register_tenant.html', {'form': form})

@login_required
def subscription_plans(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, 'saas/subscription_plans.html', {'plans': plans})

@login_required
def tenant_dashboard(request):
    if not hasattr(request, 'tenant'):
        return redirect('register_tenant')
        
    context = {
        'tenant': request.tenant,
        'subscription': request.tenant.subscription_plan,
        'users': TenantUser.objects.filter(tenant=request.tenant)
    }
    return render(request, 'saas/dashboard.html', context)
