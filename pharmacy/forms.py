from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import (
    Medicine,
    Inventory,
    Prescription,
    PrescriptionItem,
    InventoryTransaction,
)


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ["name", "description", "category", "unit", "price"]

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price and price < 0:
            raise forms.ValidationError(_("السعر يجب أن يكون أكبر من صفر"))
        return price


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ["medicine", "quantity", "batch_number", "expiry_date"]

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        if quantity and quantity < 0:
            raise forms.ValidationError(_("الكمية يجب أن تكون أكبر من صفر"))
        return quantity


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ["patient", "doctor", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class PrescriptionItemForm(forms.ModelForm):
    class Meta:
        model = PrescriptionItem
        fields = ["medicine", "quantity", "dosage_instructions", "duration"]
        widgets = {
            "dosage_instructions": forms.Textarea(attrs={"rows": 2}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        if quantity and quantity < 0:
            raise forms.ValidationError(_("الكمية يجب أن تكون أكبر من صفر"))
        return quantity


PrescriptionItemFormSet = inlineformset_factory(
    Prescription, PrescriptionItem, form=PrescriptionItemForm, extra=1, can_delete=True
)


class InventoryTransactionForm(forms.ModelForm):
    class Meta:
        model = InventoryTransaction
        fields = ["inventory", "quantity", "transaction_type", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        if quantity and quantity < 0:
            raise forms.ValidationError(_("الكمية يجب أن تكون أكبر من صفر"))
        return quantity


class InventorySearchForm(forms.Form):
    search = forms.CharField(required=False, label=_("بحث"))
    category = forms.ChoiceField(
        required=False,
        choices=[("", _("-- اختر الفئة --"))] + Medicine.CATEGORY_CHOICES,
        label=_("الفئة"),
    )
    low_stock = forms.BooleanField(required=False, label=_("المخزون المنخفض فقط"))


class PrescriptionSearchForm(forms.Form):
    search = forms.CharField(required=False, label=_("بحث"))
    status = forms.ChoiceField(
        required=False,
        choices=[("", _("-- اختر الحالة --"))] + Prescription.STATUS_CHOICES,
        label=_("الحالة"),
    )
    date_from = forms.DateField(required=False, label=_("من تاريخ"))
    date_to = forms.DateField(required=False, label=_("إلى تاريخ"))
