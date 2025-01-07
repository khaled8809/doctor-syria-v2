from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.utils import timezone

class Medicine(models.Model):
    """نموذج الأدوية"""
    
    CATEGORY_CHOICES = [
        ('tablet', _('Tablet')),
        ('capsule', _('Capsule')),
        ('syrup', _('Syrup')),
        ('injection', _('Injection')),
        ('cream', _('Cream')),
        ('drops', _('Drops')),
        ('inhaler', _('Inhaler')),
        ('other', _('Other')),
    ]
    
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    scientific_name = models.CharField(max_length=255, verbose_name=_('Scientific Name'))
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='tablet',
        verbose_name=_('Category')
    )
    manufacturer = models.CharField(max_length=255, verbose_name=_('Manufacturer'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    dosage = models.CharField(max_length=100, verbose_name=_('Dosage'))
    unit = models.CharField(max_length=50, verbose_name=_('Unit'))
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_('Price')
    )
    requires_prescription = models.BooleanField(
        default=True,
        verbose_name=_('Requires Prescription')
    )
    side_effects = models.TextField(blank=True, verbose_name=_('Side Effects'))
    storage_instructions = models.TextField(blank=True, verbose_name=_('Storage Instructions'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.dosage})"

    class Meta:
        verbose_name = _('Medicine')
        verbose_name_plural = _('Medicines')
        ordering = ['name']

class Inventory(models.Model):
    """نموذج المخزون"""
    
    medicine = models.OneToOneField(
        Medicine,
        on_delete=models.CASCADE,
        related_name='inventory',
        verbose_name=_('Medicine')
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Quantity')
    )
    minimum_stock = models.PositiveIntegerField(
        default=10,
        verbose_name=_('Minimum Stock Level')
    )
    batch_number = models.CharField(
        max_length=100,
        verbose_name=_('Batch Number')
    )
    expiry_date = models.DateField(verbose_name=_('Expiry Date'))
    last_restock_date = models.DateField(
        auto_now=True,
        verbose_name=_('Last Restock Date')
    )

    def __str__(self):
        return f"{self.medicine.name} - {self.quantity} {self.medicine.unit}s"

    def is_low_stock(self):
        return self.quantity <= self.minimum_stock

    class Meta:
        verbose_name = _('Inventory')
        verbose_name_plural = _('Inventories')

class Prescription(models.Model):
    """نموذج الوصفات الطبية"""
    
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('dispensed', _('Dispensed')),
        ('cancelled', _('Cancelled')),
    ]
    
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='prescriptions',
        verbose_name=_('Patient')
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='prescribed_medications',
        verbose_name=_('Doctor')
    )
    date_prescribed = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date Prescribed')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Status')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notes')
    )
    dispensed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dispensed_prescriptions',
        verbose_name=_('Dispensed By')
    )
    dispensed_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Dispensed Date')
    )

    def __str__(self):
        return f"Prescription for {self.patient.get_full_name()} - {self.date_prescribed.date()}"

    class Meta:
        verbose_name = _('Prescription')
        verbose_name_plural = _('Prescriptions')
        ordering = ['-date_prescribed']

class PrescriptionItem(models.Model):
    """نموذج عناصر الوصفة الطبية"""
    
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Prescription')
    )
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        verbose_name=_('Medicine')
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name=_('Quantity')
    )
    dosage_instructions = models.TextField(verbose_name=_('Dosage Instructions'))
    duration = models.CharField(
        max_length=100,
        verbose_name=_('Duration')
    )

    def __str__(self):
        return f"{self.medicine.name} - {self.quantity} {self.medicine.unit}s"

    class Meta:
        verbose_name = _('Prescription Item')
        verbose_name_plural = _('Prescription Items')

class InventoryTransaction(models.Model):
    """نموذج حركات المخزون"""
    
    TRANSACTION_TYPES = [
        ('in', _('Stock In')),
        ('out', _('Stock Out')),
        ('adjustment', _('Adjustment')),
    ]
    
    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name=_('Inventory')
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES,
        verbose_name=_('Transaction Type')
    )
    quantity = models.IntegerField(verbose_name=_('Quantity'))
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date')
    )
    reference = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Reference')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notes')
    )
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Performed By')
    )

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.inventory.medicine.name}"

    class Meta:
        verbose_name = _('Inventory Transaction')
        verbose_name_plural = _('Inventory Transactions')
        ordering = ['-date']
