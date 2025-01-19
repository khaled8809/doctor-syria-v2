from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from .models import (
    Inventory,
    InventoryTransaction,
    Medicine,
    Prescription,
    PrescriptionItem,
)


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = [
            "name",
            "scientific_name",
            "manufacturer",
            "description",
            "dosage_form",
            "strength",
            "price",
            "requires_prescription",
        ]

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price and price < 0:
            raise forms.ValidationError(_("السعر يجب أن يكون أكبر من صفر"))
        return price


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = [
            "medicine",
            "batch_number",
            "expiry_date",
            "quantity",
            "reorder_level",
            "unit_cost",
        ]

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        if quantity and quantity < 0:
            raise forms.ValidationError(_("الكمية يجب أن تكون أكبر من صفر"))
        return quantity

    def clean_unit_cost(self):
        unit_cost = self.cleaned_data.get("unit_cost")
        if unit_cost and unit_cost < 0:
            raise forms.ValidationError(_("تكلفة الوحدة يجب أن تكون أكبر من صفر"))
        return unit_cost


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ["patient", "doctor", "diagnosis", "notes"]
        widgets = {
            "diagnosis": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class PrescriptionItemForm(forms.ModelForm):
    class Meta:
        model = PrescriptionItem
        fields = [
            "medicine",
            "quantity",
            "dosage",
            "frequency",
            "duration",
            "instructions",
        ]
        widgets = {
            "instructions": forms.Textarea(attrs={"rows": 2}),
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
        fields = [
            "inventory",
            "transaction_type",
            "quantity",
            "unit_price",
            "reference",
            "notes",
        ]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        if quantity and quantity < 0:
            raise forms.ValidationError(_("الكمية يجب أن تكون أكبر من صفر"))
        return quantity

    def clean_unit_price(self):
        unit_price = self.cleaned_data.get("unit_price")
        if unit_price and unit_price < 0:
            raise forms.ValidationError(_("سعر الوحدة يجب أن يكون أكبر من صفر"))
        return unit_price


class InventorySearchForm(forms.Form):
    search = forms.CharField(required=False, label=_("بحث"))
    low_stock = forms.BooleanField(required=False, label=_("المخزون المنخفض فقط"))
    expiry_date_from = forms.DateField(required=False, label=_("تاريخ الانتهاء من"))
    expiry_date_to = forms.DateField(required=False, label=_("تاريخ الانتهاء إلى"))


class PrescriptionSearchForm(forms.Form):
    search = forms.CharField(required=False, label=_("بحث"))
    is_active = forms.BooleanField(required=False, label=_("الوصفات الفعالة فقط"))
    date_from = forms.DateField(required=False, label=_("من تاريخ"))
    date_to = forms.DateField(required=False, label=_("إلى تاريخ"))
