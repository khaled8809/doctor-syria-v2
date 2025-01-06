"""
Views for the accounts app
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.utils import timezone
from datetime import timedelta
from accounts.models import User

# سيتم إضافة المزيد من الـ views لاحقاً

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('accounts:dashboard')
    return render(request, 'registration/login.html')

@login_required
def dashboard(request):
    context = {
        'today_appointments_count': 0,  # سيتم تحديثه لاحقاً
        'new_prescriptions_count': 0,   # سيتم تحديثه لاحقاً
        'active_patients_count': User.objects.filter(role='patient', is_active=True).count(),
        'doctors_count': User.objects.filter(role='doctor', is_active=True).count(),
        'upcoming_appointments': [],     # سيتم تحديثه لاحقاً
        'notifications': [],            # سيتم تحديثه لاحقاً
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})
