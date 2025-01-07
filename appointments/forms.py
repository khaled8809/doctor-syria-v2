from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Appointment, WaitingList

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'reason', 'priority']
        widgets = {
            'appointment_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and not user.is_staff:
            if hasattr(user, 'doctor_appointments'):
                self.fields.pop('doctor')
            else:
                # فلترة الأطباء المتاحين فقط
                self.fields['doctor'].queryset = self.fields['doctor'].queryset.filter(
                    is_staff=True,
                    schedules__is_available=True
                ).distinct()

    def clean_appointment_date(self):
        date = self.cleaned_data.get('appointment_date')
        if date and date < timezone.now():
            raise forms.ValidationError(_('لا يمكن حجز موعد في وقت سابق'))
        return date

class WaitingListForm(forms.ModelForm):
    class Meta:
        model = WaitingList
        fields = ['doctor', 'reason', 'priority', 'preferred_date', 'notes']
        widgets = {
            'preferred_date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'reason': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and not user.is_staff:
            # فلترة الأطباء المتاحين فقط
            self.fields['doctor'].queryset = self.fields['doctor'].queryset.filter(
                is_staff=True
            ).distinct()

    def clean_preferred_date(self):
        date = self.cleaned_data.get('preferred_date')
        if date and date < timezone.now().date():
            raise forms.ValidationError(_('لا يمكن اختيار تاريخ سابق'))
