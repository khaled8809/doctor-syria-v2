from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .models import (
    Employee, Leave, Shift, Attendance, Payroll,
    Evaluation, Training
)

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'employee_id', 'department', 'position', 'employment_type',
            'join_date', 'end_date', 'gender', 'date_of_birth',
            'marital_status', 'phone', 'emergency_contact', 'address',
            'basic_salary', 'bank_account', 'is_active', 'notes'
        ]
        widgets = {
            'join_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = [
            'leave_type', 'start_date', 'end_date',
            'reason', 'notes'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError(
                    _('End date must be after start date')
                )
            if start_date < timezone.now().date():
                raise forms.ValidationError(
                    _('Start date cannot be in the past')
                )

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = [
            'name', 'start_time', 'end_time',
            'break_duration', 'is_night_shift', 'description'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = [
            'employee', 'date', 'shift', 'check_in',
            'check_out', 'status', 'notes'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'check_in': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'check_out': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = [
            'employee', 'period_start', 'period_end',
            'basic_salary', 'overtime_hours', 'overtime_rate',
            'allowances', 'deductions', 'payment_method',
            'payment_status', 'notes'
        ]
        widgets = {
            'period_start': forms.DateInput(attrs={'type': 'date'}),
            'period_end': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        period_start = cleaned_data.get('period_start')
        period_end = cleaned_data.get('period_end')
        
        if period_start and period_end:
            if period_start > period_end:
                raise forms.ValidationError(
                    _('End date must be after start date')
                )

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = [
            'employee', 'evaluation_date', 'period_start', 'period_end',
            'performance_score', 'attendance_score', 'punctuality_score',
            'productivity_score', 'quality_score', 'initiative_score',
            'teamwork_score', 'communication_score', 'strengths',
            'areas_for_improvement', 'goals', 'comments'
        ]
        widgets = {
            'evaluation_date': forms.DateInput(attrs={'type': 'date'}),
            'period_start': forms.DateInput(attrs={'type': 'date'}),
            'period_end': forms.DateInput(attrs={'type': 'date'}),
            'strengths': forms.Textarea(attrs={'rows': 3}),
            'areas_for_improvement': forms.Textarea(attrs={'rows': 3}),
            'goals': forms.Textarea(attrs={'rows': 3}),
            'comments': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        period_start = cleaned_data.get('period_start')
        period_end = cleaned_data.get('period_end')
        evaluation_date = cleaned_data.get('evaluation_date')
        
        if period_start and period_end and evaluation_date:
            if period_start > period_end:
                raise forms.ValidationError(
                    _('Period end must be after period start')
                )
            if evaluation_date < period_end:
                raise forms.ValidationError(
                    _('Evaluation date must be after period end')
                )

class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = [
            'title', 'description', 'trainer', 'start_date',
            'end_date', 'location', 'participants', 'max_participants',
            'cost', 'status', 'materials', 'prerequisites',
            'objectives', 'notes'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'materials': forms.Textarea(attrs={'rows': 3}),
            'prerequisites': forms.Textarea(attrs={'rows': 3}),
            'objectives': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        max_participants = cleaned_data.get('max_participants')
        participants = cleaned_data.get('participants')
        
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError(
                    _('End date must be after start date')
                )
            if start_date < timezone.now().date():
                raise forms.ValidationError(
                    _('Start date cannot be in the past')
                )
        
        if participants and max_participants:
            if participants.count() > max_participants:
                raise forms.ValidationError(
                    _('Number of participants exceeds maximum limit')
                )

class EmployeeSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label=_('بحث'),
        widget=forms.TextInput(attrs={'placeholder': _('ابحث عن موظف...')})
    )
    department = forms.CharField(
        required=False,
        label=_('القسم')
    )
    employment_type = forms.ChoiceField(
        required=False,
        label=_('نوع التوظيف'),
        choices=[('', _('الكل'))] + Employee.EMPLOYMENT_TYPE_CHOICES
    )
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        label=_('النشطين فقط')
    )

class LeaveSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label=_('بحث'),
        widget=forms.TextInput(attrs={'placeholder': _('ابحث عن إجازة...')})
    )
    leave_type = forms.ChoiceField(
        required=False,
        label=_('نوع الإجازة'),
        choices=[('', _('الكل'))] + Leave.LEAVE_TYPE_CHOICES
    )
    status = forms.ChoiceField(
        required=False,
        label=_('الحالة'),
        choices=[('', _('الكل'))] + Leave.STATUS_CHOICES
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
