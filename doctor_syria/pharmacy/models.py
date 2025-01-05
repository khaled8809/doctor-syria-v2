from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import Pharmacy, PharmaceuticalCompany

class Medicine(models.Model):
    name = models.CharField(max_length=200)
    scientific_name = models.CharField(max_length=200)
    manufacturer = models.ForeignKey(PharmaceuticalCompany, on_delete=models.CASCADE, related_name='medicines')
    description = models.TextField()
    dosage_form = models.CharField(max_length=100)  # e.g., tablet, syrup, injection
    strength = models.CharField(max_length=100)  # e.g., 500mg, 10ml
    price = models.DecimalField(max_digits=10, decimal_places=2)
    requires_prescription = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.strength}"

class PharmacyInventory(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name='inventory')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='pharmacy_inventory')
    quantity = models.PositiveIntegerField()
    batch_number = models.CharField(max_length=100)
    expiry_date = models.DateField()
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Pharmacy Inventories'
    
    def __str__(self):
        return f"{self.medicine} - {self.pharmacy}"

class MedicineOrder(models.Model):
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('shipped', _('Shipped')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    )
    
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Order {self.id} - {self.pharmacy}"

class OrderItem(models.Model):
    order = models.ForeignKey(MedicineOrder, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def total_price(self):
        return self.quantity * self.price_per_unit
    
    def __str__(self):
        return f"{self.medicine} x {self.quantity}"

class DeliveryAddress(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name='delivery_addresses')
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Delivery Addresses'
    
    def __str__(self):
        return f"{self.pharmacy} - {self.street_address}"

class MedicineCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    class Meta:
        verbose_name_plural = 'Medicine Categories'
    
    def __str__(self):
        return self.name

class MedicineCategoryRelation(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey(MedicineCategory, on_delete=models.CASCADE, related_name='medicines')
    
    class Meta:
        unique_together = ('medicine', 'category')
    
    def __str__(self):
        return f"{self.medicine} - {self.category}"
