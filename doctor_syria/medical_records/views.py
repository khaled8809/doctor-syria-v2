from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import MedicalRecord
from .forms import MedicalRecordForm

class RecordListView(LoginRequiredMixin, ListView):
    model = MedicalRecord
    template_name = 'medical_records/record_list.html'
    context_object_name = 'records'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return MedicalRecord.objects.filter(doctor=user.doctor)
        elif user.role == 'patient':
            return MedicalRecord.objects.filter(patient=user.patient)
        return MedicalRecord.objects.none()

class RecordDetailView(LoginRequiredMixin, DetailView):
    model = MedicalRecord
    template_name = 'medical_records/record_detail.html'
    context_object_name = 'record'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return MedicalRecord.objects.filter(doctor=user.doctor)
        elif user.role == 'patient':
            return MedicalRecord.objects.filter(patient=user.patient)
        return MedicalRecord.objects.none()

class RecordCreateView(LoginRequiredMixin, CreateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'medical_records/record_form.html'
    success_url = reverse_lazy('medical_records:record_list')

    def form_valid(self, form):
        form.instance.doctor = self.request.user.doctor
        return super().form_valid(form)

class RecordUpdateView(LoginRequiredMixin, UpdateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'medical_records/record_form.html'
    success_url = reverse_lazy('medical_records:record_list')

    def get_queryset(self):
        return MedicalRecord.objects.filter(doctor=self.request.user.doctor)

class RecordDeleteView(LoginRequiredMixin, DeleteView):
    model = MedicalRecord
    template_name = 'medical_records/record_confirm_delete.html'
    success_url = reverse_lazy('medical_records:record_list')

    def get_queryset(self):
        return MedicalRecord.objects.filter(doctor=self.request.user.doctor)
