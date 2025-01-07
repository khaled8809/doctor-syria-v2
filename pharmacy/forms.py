from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import Medicine, Inventory, Prescription, PrescriptionItem, InventoryTransaction

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = [
            'name', 'scientific_name', 'category', 'manufacturer',
            'description', 'dosage', 'unit', 'price', 'requires_prescription',
            'side_effects', 'storage_instructions'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'side_effects': forms.Textarea(attrs={'rows': 3}),
            'storage_instructions': forms.Textarea(attrs={'rows': 3}),
        }

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['medicine', 'quantity', 'minimum_stock', 'batch_number', 'expiry_date']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get('expiry_date')
        if expiry_date and expiry_date < timezone.now().date():
            raise ValidationError(_('تاريخ انتهاء الصلاحية يجب أن يكون في المستقبل'))
        return expiry_date

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and not user.is_staff:
            self.fields['patient'].initial = user
            self.fields['patient'].widget = forms.HiddenInput()

class PrescriptionItemForm(forms.ModelForm):
    class Meta:
        model = PrescriptionItem
        fields = ['medicine', 'quantity', 'dosage_instructions', 'duration']
        widgets = {
            'dosage_instructions': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # فلترة الأدوية المتوفرة في المخزون فقط
        self.fields['medicine'].queryset = Medicine.objects.filter(
            inventory__quantity__gt=0
        )

    def clean(self):
        cleaned_data = super().clean()
        medicine = cleaned_data.get('medicine')
        quantity = cleaned_data.get('quantity')

        if medicine and quantity:
            inventory = medicine.inventory
            if inventory.quantity < quantity:
                raise ValidationError(
                    _('الكمية المطلوبة غير متوفرة في المخزون. المتوفر: %(available)s'),
                    params={'available': inventory.quantity},
                )

class InventoryTransactionForm(forms.ModelForm):
    class Meta:
        model = InventoryTransaction
        fields = ['inventory', 'transaction_type', 'quantity', 'reference', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        inventory = cleaned_data.get('inventory')
        transaction_type = cleaned_data.get('transaction_type')
        quantity = cleaned_data.get('quantity')

        if inventory and transaction_type == 'out' and quantity:
            if inventory.quantity < quantity:
                raise ValidationError(
                    _('الكمية المطلوبة للإخراج أكبر من المتوفر في المخزون')
                )

class InventorySearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label=_('بحث'),
        widget=forms.TextInput(attrs={'placeholder': _('ابحث عن دواء...')})
    )
    category = forms.ChoiceField(
        required=False,
        label=_('الفئة'),
        choices=[('', _('الكل'))] + Medicine.CATEGORY_CHOICES
    )
    low_stock = forms.BooleanField(
        required=False,
        label=_('المخزون المنخفض فقط')
    )
    expired = forms.BooleanField(
        required=False,
        label=_('المنتهي الصلاحية فقط')
    )

class PrescriptionSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label=_('بحث'),
        widget=forms.TextInput(attrs={'placeholder': _('ابحث عن وصفة...')})
    )
    status = forms.ChoiceField(
        required=False,
        label=_('الحالة'),
        choices=[('', _('الكل'))] + Prescription.STATUS_CHOICES
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
