from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .models import ClinicalDecision, LabResultAnalysis, TreatmentProtocol


class ClinicalDecisionListView(LoginRequiredMixin, ListView):
    model = ClinicalDecision
    template_name = "decision_support/decision_list.html"
    context_object_name = "decisions"

    def get_queryset(self):
        return ClinicalDecision.objects.filter(doctor=self.request.user)


class ClinicalDecisionCreateView(LoginRequiredMixin, CreateView):
    model = ClinicalDecision
    template_name = "decision_support/decision_form.html"
    fields = ["patient", "symptoms", "suggested_diagnosis", "recommended_tests"]
    success_url = reverse_lazy("decision_support:decision-list")

    def form_valid(self, form):
        form.instance.doctor = self.request.user
        return super().form_valid(form)


class TreatmentProtocolListView(LoginRequiredMixin, ListView):
    model = TreatmentProtocol
    template_name = "decision_support/protocol_list.html"
    context_object_name = "protocols"

    def get_queryset(self):
        queryset = super().get_queryset()
        condition = self.request.GET.get("condition")
        if condition:
            queryset = queryset.filter(condition__icontains=condition)
        return queryset


class LabResultAnalysisListView(LoginRequiredMixin, ListView):
    model = LabResultAnalysis
    template_name = "decision_support/lab_analysis_list.html"
    context_object_name = "analyses"

    def get_queryset(self):
        return LabResultAnalysis.objects.filter(
            lab_result__patient__doctor=self.request.user
        ).select_related("lab_result")
