from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .models import BedManagement, MedicalEquipment, OperatingRoom


class ResourceListView(LoginRequiredMixin, ListView):
    template_name = "resource_management/resource_list.html"
    context_object_name = "resources"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["equipment_count"] = MedicalEquipment.objects.count()
        context["operating_rooms_count"] = OperatingRoom.objects.count()
        context["beds_count"] = BedManagement.objects.count()
        context["available_beds"] = BedManagement.objects.filter(
            status="Available"
        ).count()
        return context

    def get_queryset(self):
        return []


class MedicalEquipmentListView(LoginRequiredMixin, ListView):
    model = MedicalEquipment
    template_name = "resource_management/equipment_list.html"
    context_object_name = "equipment_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["maintenance_needed"] = self.model.objects.filter(status="Maintenance")
        return context


class OperatingRoomListView(LoginRequiredMixin, ListView):
    model = OperatingRoom
    template_name = "resource_management/operating_room_list.html"
    context_object_name = "operating_rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["available_rooms"] = self.model.objects.filter(status="Available")
        return context


class BedManagementListView(LoginRequiredMixin, ListView):
    model = BedManagement
    template_name = "resource_management/bed_list.html"
    context_object_name = "beds"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["available_beds"] = self.model.objects.filter(
            status="Available"
        ).count()
        context["occupied_beds"] = self.model.objects.filter(status="Occupied").count()
        return context


class BedAssignmentView(LoginRequiredMixin, UpdateView):
    model = BedManagement
    template_name = "resource_management/bed_assignment.html"
    fields = ["current_patient", "status"]
    success_url = reverse_lazy("resource_management:bed-list")

    def form_valid(self, form):
        if form.cleaned_data["current_patient"]:
            form.instance.status = "Occupied"
        else:
            form.instance.status = "Available"
        return super().form_valid(form)
