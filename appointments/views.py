from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Appointment, Schedule, WaitingList
from .forms import AppointmentForm, WaitingListForm

class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/appointment_list.html'
    context_object_name = 'appointments'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Appointment.objects.all().order_by('-appointment_date')
        elif hasattr(user, 'doctor_appointments'):
            return user.doctor_appointments.all().order_by('-appointment_date')
        else:
            return user.patient_appointments.all().order_by('-appointment_date')

class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/appointment_form.html'
    success_url = reverse_lazy('appointments:list')

    def form_valid(self, form):
        appointment = form.save(commit=False)
        if not self.request.user.is_staff:
            appointment.patient = self.request.user
        appointment.save()
        messages.success(self.request, 'تم حجز الموعد بنجاح.')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'appointments/appointment_detail.html'
    context_object_name = 'appointment'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Appointment.objects.all()
        return Appointment.objects.filter(
            Q(patient=user) | Q(doctor=user)
        )

class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/appointment_form.html'
    success_url = reverse_lazy('appointments:list')

    def get_queryset(self):
        if self.request.user.is_staff:
            return Appointment.objects.all()
        return Appointment.objects.filter(
            Q(patient=self.request.user) | Q(doctor=self.request.user),
            status='pending'
        )

    def form_valid(self, form):
        messages.success(self.request, 'تم تحديث الموعد بنجاح.')
        return super().form_valid(form)

class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'appointments/appointment_confirm_delete.html'
    success_url = reverse_lazy('appointments:list')

    def get_queryset(self):
        if self.request.user.is_staff:
            return Appointment.objects.all()
        return Appointment.objects.filter(
            Q(patient=self.request.user) | Q(doctor=self.request.user),
            status='pending'
        )

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'تم إلغاء الموعد بنجاح.')
        return super().delete(request, *args, **kwargs)

class AppointmentCalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'appointments/appointment_calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_staff:
            appointments = Appointment.objects.all()
        elif hasattr(user, 'doctor_appointments'):
            appointments = user.doctor_appointments.all()
        else:
            appointments = user.patient_appointments.all()

        # تحويل المواعيد إلى تنسيق يناسب التقويم
        calendar_events = []
        for appointment in appointments:
            event = {
                'id': appointment.id,
                'title': f"{appointment.patient.get_full_name()} - {appointment.reason}",
                'start': appointment.appointment_date.isoformat(),
                'end': (appointment.appointment_date + timezone.timedelta(minutes=30)).isoformat(),
                'status': appointment.status,
            }
            calendar_events.append(event)
        
        context['calendar_events'] = calendar_events
        return context

class MyAppointmentsView(LoginRequiredMixin, ListView):
    template_name = 'appointments/my_appointments.html'
    context_object_name = 'appointments'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        return Appointment.objects.filter(
            Q(patient=user) | Q(doctor=user)
        ).filter(
            appointment_date__gte=timezone.now()
        ).order_by('appointment_date')
