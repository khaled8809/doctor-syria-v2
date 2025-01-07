from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .models import Test, TestRequest, TestResult, LabEquipment, QualityControl

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = [
            'name', 'code', 'category', 'description', 'price',
            'preparation_instructions', 'normal_range', 'unit',
            'processing_time', 'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'preparation_instructions': forms.Textarea(attrs={'rows': 3}),
        }

class TestRequestForm(forms.ModelForm):
    class Meta:
        model = TestRequest
        fields = ['patient', 'tests', 'priority', 'notes', 'scheduled_for']
        widgets = {
            'scheduled_for': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
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

        # فلترة التحاليل النشطة فقط
        self.fields['tests'].queryset = Test.objects.filter(is_active=True)

    def clean_scheduled_for(self):
        scheduled_for = self.cleaned_data.get('scheduled_for')
        if scheduled_for and scheduled_for < timezone.now():
            raise forms.ValidationError(_('لا يمكن جدولة التحليل في وقت سابق'))
        return scheduled_for

class TestResultForm(forms.ModelForm):
    class Meta:
        model = TestResult
        fields = ['value', 'is_normal', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class LabEquipmentForm(forms.ModelForm):
    class Meta:
        model = LabEquipment
        fields = [
            'name', 'model', 'serial_number', 'manufacturer',
            'purchase_date', 'last_maintenance', 'next_maintenance',
            'status', 'notes'
        ]
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'last_maintenance': forms.DateInput(attrs={'type': 'date'}),
            'next_maintenance': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class QualityControlForm(forms.ModelForm):
    class Meta:
        model = QualityControl
        fields = [
            'test', 'equipment', 'control_date', 'control_value',
            'expected_range', 'is_passed', 'notes'
        ]
        widgets = {
            'control_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class TestSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label=_('بحث'),
        widget=forms.TextInput(attrs={'placeholder': _('ابحث عن تحليل...')})
    )
    category = forms.ChoiceField(
        required=False,
        label=_('الفئة'),
        choices=[('', _('الكل'))] + Test.CATEGORY_CHOICES
    )
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        label=_('النشطة فقط')
    )

class TestRequestSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label=_('بحث'),
        widget=forms.TextInput(attrs={'placeholder': _('ابحث عن طلب...')})
    )
    status = forms.ChoiceField(
        required=False,
        label=_('الحالة'),
        choices=[('', _('الكل'))] + TestRequest.STATUS_CHOICES
    )
    priority = forms.ChoiceField(
        required=False,
        label=_('الأولوية'),
        choices=[('', _('الكل'))] + TestRequest.PRIORITY_CHOICES
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
            raise forms.ValidationError(_('تاريخ البداية يجب أن يكون قبل تاريخ النهاية'))
