from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Specialty
from .serializers import SpecialtySerializer

def error_404(request, exception):
    return render(request, "errors/404.html", status=404)


def error_500(request):
    return render(request, "errors/500.html", status=500)


@login_required
def help_home(request):
    return render(request, "help/home.html")


@login_required
def support(request):
    return render(request, "help/support.html")


@login_required
def general_settings(request):
    if request.method == "POST":
        # هنا يتم معالجة البيانات المرسلة من النموذج
        # TODO: أضف منطق حفظ الإعدادات
        pass

    return render(request, "settings/general.html")


def home(request):
    """View for home page"""
    return render(request, 'core/home.html', {
        'title': 'Doctor Syria - Your Health Partner'
    })


def privacy_policy(request):
    """View for privacy policy page"""
    return render(request, 'core/privacy_policy.html', {
        'title': 'Privacy Policy',
        'last_updated': '2025-01-19'
    })


def terms(request):
    return render(request, "legal/terms.html")


def faq(request):
    return render(request, "help/faq.html")


class SpecialtyViewSet(viewsets.ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class SpecialtyListView(ListView):
    model = Specialty
    template_name = 'core/specialty_list.html'
    context_object_name = 'specialties'
    ordering = ['name']
