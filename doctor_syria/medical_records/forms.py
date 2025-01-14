from django import forms

from .models import MedicalRecord


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ["patient", "diagnosis", "treatment", "notes", "date"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 4}),
            "treatment": forms.Textarea(attrs={"rows": 4}),
        }
