from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView

from .models import Course, MedicalLibrary, VirtualSimulation


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "medical_education/course_list.html"
    context_object_name = "courses"


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "medical_education/course_detail.html"
    context_object_name = "course"


class VirtualSimulationListView(LoginRequiredMixin, ListView):
    model = VirtualSimulation
    template_name = "medical_education/simulation_list.html"
    context_object_name = "simulations"


class MedicalLibraryListView(LoginRequiredMixin, ListView):
    model = MedicalLibrary
    template_name = "medical_education/library_list.html"
    context_object_name = "resources"

    def get_queryset(self):
        queryset = super().get_queryset()
        content_type = self.request.GET.get("type")
        if content_type:
            queryset = queryset.filter(content_type=content_type)
        return queryset
