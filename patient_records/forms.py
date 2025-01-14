from django import forms

from .models import MedicalRecord, MedicalVisit


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = [
            "patient",
            "blood_type",
            "height",
            "weight",
            "allergies",
            "chronic_conditions",
        ]
        widgets = {
            "allergies": forms.Textarea(attrs={"rows": 3}),
            "chronic_conditions": forms.Textarea(attrs={"rows": 3}),
        }


class MedicalVisitForm(forms.ModelForm):
    class Meta:
        model = MedicalVisit
        fields = [
            "patient",
            "doctor",
            "visit_type",
            "visit_date",
            "symptoms",
            "diagnosis",
            "treatment",
            "notes",
            "follow_up_date",
        ]
        widgets = {
            "visit_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "follow_up_date": forms.DateInput(attrs={"type": "date"}),
            "symptoms": forms.Textarea(attrs={"rows": 3}),
            "diagnosis": forms.Textarea(attrs={"rows": 3}),
            "treatment": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
