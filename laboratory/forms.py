from django import forms
from django.utils.translation import gettext_lazy as _

from .models import LabResult, LabTest


class LabTestForm(forms.ModelForm):
    class Meta:
        model = LabTest
        fields = [
            "name",
            "code",
            "category",
            "description",
            "price",
            "normal_range",
            "unit",
            "is_active",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class LabResultForm(forms.ModelForm):
    class Meta:
        model = LabResult
        fields = ["patient", "test", "value", "status", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class TestSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label=_("بحث"),
        widget=forms.TextInput(attrs={"placeholder": _("ابحث عن تحليل...")}),
    )
    category = forms.ChoiceField(
        required=False,
        label=_("الفئة"),
        choices=[("", _("الكل"))] + LabTest.TEST_CATEGORIES,
    )
    is_active = forms.BooleanField(required=False, label=_("نشط فقط"))


class ResultSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label=_("بحث"),
        widget=forms.TextInput(attrs={"placeholder": _("ابحث عن نتيجة...")}),
    )
    status = forms.ChoiceField(
        required=False,
        label=_("الحالة"),
        choices=[("", _("الكل"))] + LabResult.RESULT_STATUS,
    )
    date_from = forms.DateField(
        required=False,
        label=_("من تاريخ"),
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    date_to = forms.DateField(
        required=False,
        label=_("إلى تاريخ"),
        widget=forms.DateInput(attrs={"type": "date"}),
    )
