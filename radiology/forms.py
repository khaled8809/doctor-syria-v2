from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .models import (
    RadiologyExamination, RadiologyRequest, RadiologyResult,
    RadiologyImage, RadiologyEquipment, EquipmentMaintenance
)

class RadiologyExaminationForm(forms.ModelForm):
    class Meta:
        model = RadiologyExamination
        fields = [
            'name', 'code', 'category', 'body_part', 'description',
            'price', 'preparation_instructions', 'radiation_dose',
            'duration', 'requires_contrast', 'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'preparation_instructions': forms.Textarea(attrs={'rows': 3}),
        }

class RadiologyRequestForm(forms.ModelForm):
    class Meta:
        model = RadiologyRequest
        fields = [
            'patient', 'examination', 'priority', 'clinical_history',
            'clinical_findings', 'notes', 'scheduled_for'
        ]
        widgets = {
            'scheduled_for': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'clinical_history': forms.Textarea(attrs={'rows': 3}),
            'clinical_findings': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and not user.is_staff:
            if hasattr(user, 'doctor_profile'):
                self.fields.pop('doctor')
            else:
                self.fields['patient'].initial = user
                self.fields['patient'].widget = forms.HiddenInput()

        # فلترة الفحوصات النشطة فقط
        self.fields['examination'].queryset = RadiologyExamination.objects.filter(
            is_active=True
        )

    def clean_scheduled_for(self):
        scheduled_for = self.cleaned_data.get('scheduled_for')
        if scheduled_for and scheduled_for < timezone.now():
            raise forms.ValidationError(
                _('لا يمكن جدولة الفحص في وقت سابق')
            )
        return scheduled_for

class RadiologyResultForm(forms.ModelForm):
    class Meta:
        model = RadiologyResult
        fields = [
            'findings', 'impression', 'recommendations',
            'technical_notes', 'radiation_dose', 'contrast_used',
            'contrast_type', 'contrast_volume'
        ]
        widgets = {
            'findings': forms.Textarea(attrs={'rows': 4}),
            'impression': forms.Textarea(attrs={'rows': 4}),
            'recommendations': forms.Textarea(attrs={'rows': 3}),
            'technical_notes': forms.Textarea(attrs={'rows': 3}),
        }

class RadiologyImageForm(forms.ModelForm):
    class Meta:
        model = RadiologyImage
        fields = ['image', 'description', 'sequence_number']

class RadiologyEquipmentForm(forms.ModelForm):
    class Meta:
        model = RadiologyEquipment
        fields = [
            'name', 'model', 'manufacturer', 'serial_number',
            'equipment_type', 'installation_date', 'warranty_expiry',
            'last_maintenance', 'next_maintenance', 'calibration_date',
            'room_number', 'status', 'notes'
        ]
        widgets = {
            'installation_date': forms.DateInput(attrs={'type': 'date'}),
            'warranty_expiry': forms.DateInput(attrs={'type': 'date'}),
            'last_maintenance': forms.DateInput(attrs={'type': 'date'}),
            'next_maintenance': forms.DateInput(attrs={'type': 'date'}),
            'calibration_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class EquipmentMaintenanceForm(forms.ModelForm):
    class Meta:
        model = EquipmentMaintenance
        fields = [
            'maintenance_type', 'maintenance_date', 'performed_by',
            'cost', 'description', 'actions_taken', 'parts_replaced',
            'next_maintenance', 'status', 'notes'
        ]
        widgets = {
            'maintenance_date': forms.DateInput(attrs={'type': 'date'}),
            'next_maintenance': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'actions_taken': forms.Textarea(attrs={'rows': 3}),
            'parts_replaced': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class RadiologySearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label=_('بحث'),
        widget=forms.TextInput(attrs={'placeholder': _('ابحث عن فحص...')})
    )
    category = forms.ChoiceField(
        required=False,
        label=_('النوع'),
        choices=[('', _('الكل'))] + RadiologyExamination.CATEGORY_CHOICES
    )
    body_part = forms.ChoiceField(
        required=False,
        label=_('منطقة الجسم'),
        choices=[('', _('الكل'))] + RadiologyExamination.BODY_PART_CHOICES
    )
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        label=_('النشطة فقط')
    )

class RadiologyRequestSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label=_('بحث'),
        widget=forms.TextInput(attrs={'placeholder': _('ابحث عن طلب...')})
    )
    status = forms.ChoiceField(
        required=False,
        label=_('الحالة'),
        choices=[('', _('الكل'))] + RadiologyRequest.STATUS_CHOICES
    )
    priority = forms.ChoiceField(
        required=False,
        label=_('الأولوية'),
        choices=[('', _('الكل'))] + RadiologyRequest.PRIORITY_CHOICES
    )
    date_from = forms.DateField(
        required=False,
        label=_('من تاريخ'),
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    date_to = forms.DateField(
        required=False,
        label=_('إلى تاريخ'),
        widget=forms.DateInput(attrs={'type': 'date'})
    )

class DateRangeForm(forms.Form):
    date_from = forms.DateField(
        label=_('من تاريخ'),
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    date_to = forms.DateField(
        label=_('إلى تاريخ'),
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        
        if date_from and date_to and date_from > date_to:
            raise forms.ValidationError(
                _('تاريخ البداية يجب أن يكون قبل تاريخ النهاية')
            )
