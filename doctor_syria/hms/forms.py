from django import forms

from .models import (
    Admission,
    Bed,
    Department,
    Discharge,
    DoctorRound,
    Equipment,
    InventoryItem,
    MaintenanceRecord,
    NursingRound,
    Room,
    Transfer,
    Ward,
)


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = "__all__"
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class WardForm(forms.ModelForm):
    class Meta:
        model = Ward
        fields = "__all__"


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        widgets = {
            "equipment": forms.SelectMultiple(attrs={"class": "select2"}),
        }


class BedForm(forms.ModelForm):
    class Meta:
        model = Bed
        fields = "__all__"
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = "__all__"
        widgets = {
            "admission_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "expected_discharge_date": forms.DateInput(attrs={"type": "date"}),
            "diagnosis": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show available beds
        self.fields["bed"].queryset = Bed.objects.filter(status="available")


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = "__all__"
        widgets = {
            "transfer_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "reason": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show available beds for the to_bed field
        self.fields["to_bed"].queryset = Bed.objects.filter(status="available")


class NursingRoundForm(forms.ModelForm):
    class Meta:
        model = NursingRound
        fields = "__all__"
        widgets = {
            "round_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "next_round_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class DoctorRoundForm(forms.ModelForm):
    class Meta:
        model = DoctorRound
        fields = "__all__"
        widgets = {
            "round_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "next_round_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "findings": forms.Textarea(attrs={"rows": 3}),
            "instructions": forms.Textarea(attrs={"rows": 3}),
        }


class DischargeForm(forms.ModelForm):
    class Meta:
        model = Discharge
        fields = "__all__"
        widgets = {
            "discharge_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "discharge_diagnosis": forms.Textarea(attrs={"rows": 3}),
            "discharge_summary": forms.Textarea(attrs={"rows": 3}),
            "follow_up_instructions": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = "__all__"
        widgets = {
            "purchase_date": forms.DateInput(attrs={"type": "date"}),
            "last_maintenance": forms.DateInput(attrs={"type": "date"}),
            "next_maintenance": forms.DateInput(attrs={"type": "date"}),
        }


class MaintenanceRecordForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = "__all__"
        widgets = {
            "maintenance_date": forms.DateInput(attrs={"type": "date"}),
            "next_maintenance": forms.DateInput(attrs={"type": "date"}),
            "findings": forms.Textarea(attrs={"rows": 3}),
            "actions_taken": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = "__all__"
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "last_ordered": forms.DateInput(attrs={"type": "date"}),
        }


# Search Forms
class AdmissionSearchForm(forms.Form):
    patient_name = forms.CharField(required=False)
    admission_date_from = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
    admission_date_to = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
    status = forms.ChoiceField(
        choices=[("", "----")] + Admission.STATUS_CHOICES, required=False
    )


class EquipmentSearchForm(forms.Form):
    name = forms.CharField(required=False)
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(), required=False
    )
    status = forms.CharField(required=False)
    maintenance_due = forms.BooleanField(required=False)


class InventorySearchForm(forms.Form):
    name = forms.CharField(required=False)
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(), required=False
    )
    low_stock = forms.BooleanField(required=False)


# Report Forms
class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
