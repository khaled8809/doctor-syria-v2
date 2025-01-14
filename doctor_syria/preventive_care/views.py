from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .models import HealthTip, PreventiveCheckup, Vaccination


class PreventiveCareHomeView(LoginRequiredMixin, TemplateView):
    template_name = "preventive_care/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["upcoming_checkups"] = PreventiveCheckup.objects.filter(
            patient=user, completed=False
        ).order_by("due_date")[:5]
        context["upcoming_vaccinations"] = Vaccination.objects.filter(
            patient=user, completed=False
        ).order_by("due_date")[:5]
        context["latest_health_tips"] = HealthTip.objects.order_by("-created_at")[:3]
        return context


class PreventiveCheckupListView(LoginRequiredMixin, ListView):
    model = PreventiveCheckup
    template_name = "preventive_care/checkup_list.html"
    context_object_name = "checkups"

    def get_queryset(self):
        return PreventiveCheckup.objects.filter(patient=self.request.user)


class PreventiveCheckupCreateView(LoginRequiredMixin, CreateView):
    model = PreventiveCheckup
    template_name = "preventive_care/checkup_form.html"
    fields = ["checkup_type", "due_date", "notes"]
    success_url = reverse_lazy("preventive_care:checkup-list")

    def form_valid(self, form):
        form.instance.patient = self.request.user
        return super().form_valid(form)


class VaccinationListView(LoginRequiredMixin, ListView):
    model = Vaccination
    template_name = "preventive_care/vaccination_list.html"
    context_object_name = "vaccinations"

    def get_queryset(self):
        return Vaccination.objects.filter(patient=self.request.user)


class VaccinationCreateView(LoginRequiredMixin, CreateView):
    model = Vaccination
    template_name = "preventive_care/vaccination_form.html"
    fields = ["vaccine_name", "due_date", "notes"]
    success_url = reverse_lazy("preventive_care:vaccination-list")

    def form_valid(self, form):
        form.instance.patient = self.request.user
        return super().form_valid(form)


class HealthTipListView(ListView):
    model = HealthTip
    template_name = "preventive_care/health_tip_list.html"
    context_object_name = "health_tips"
