from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import LabResultForm, LabTestForm
from .models import LabResult, LabTest


class LabTestListView(LoginRequiredMixin, ListView):
    model = LabTest
    template_name = "laboratory/labtest_list.html"
    context_object_name = "tests"
    paginate_by = 10


class LabTestCreateView(LoginRequiredMixin, CreateView):
    model = LabTest
    form_class = LabTestForm
    template_name = "laboratory/labtest_form.html"
    success_url = reverse_lazy("laboratory:test-list")

    def form_valid(self, form):
        messages.success(self.request, _("تم إنشاء الفحص المخبري بنجاح."))
        return super().form_valid(form)


class LabTestDetailView(LoginRequiredMixin, DetailView):
    model = LabTest
    template_name = "laboratory/labtest_detail.html"
    context_object_name = "test"


class LabTestUpdateView(LoginRequiredMixin, UpdateView):
    model = LabTest
    form_class = LabTestForm
    template_name = "laboratory/labtest_form.html"
    success_url = reverse_lazy("laboratory:test-list")

    def form_valid(self, form):
        messages.success(self.request, _("تم تحديث الفحص المخبري بنجاح."))
        return super().form_valid(form)


class LabTestDeleteView(LoginRequiredMixin, DeleteView):
    model = LabTest
    template_name = "laboratory/labtest_confirm_delete.html"
    success_url = reverse_lazy("laboratory:test-list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, _("تم حذف الفحص المخبري بنجاح."))
        return super().delete(request, *args, **kwargs)


class LabResultListView(LoginRequiredMixin, ListView):
    model = LabResult
    template_name = "laboratory/labresult_list.html"
    context_object_name = "results"
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_staff:
            return LabResult.objects.all()
        return LabResult.objects.filter(patient=self.request.user)


class LabResultCreateView(LoginRequiredMixin, CreateView):
    model = LabResult
    form_class = LabResultForm
    template_name = "laboratory/labresult_form.html"
    success_url = reverse_lazy("laboratory:result-list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, _("تم إنشاء نتيجة الفحص بنجاح."))
        return super().form_valid(form)


class LabResultDetailView(LoginRequiredMixin, DetailView):
    model = LabResult
    template_name = "laboratory/labresult_detail.html"
    context_object_name = "result"


class LabResultUpdateView(LoginRequiredMixin, UpdateView):
    model = LabResult
    form_class = LabResultForm
    template_name = "laboratory/labresult_form.html"
    success_url = reverse_lazy("laboratory:result-list")

    def form_valid(self, form):
        messages.success(self.request, _("تم تحديث نتيجة الفحص بنجاح."))
        return super().form_valid(form)


class LabResultDeleteView(LoginRequiredMixin, DeleteView):
    model = LabResult
    template_name = "laboratory/labresult_confirm_delete.html"
    success_url = reverse_lazy("laboratory:result-list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, _("تم حذف نتيجة الفحص بنجاح."))
        return super().delete(request, *args, **kwargs)
