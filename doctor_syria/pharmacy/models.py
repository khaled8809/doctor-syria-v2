from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from core.models import TimestampMixin, SoftDeleteMixin, AuditMixin
from .choices import (
    MedicineCategory, MedicineForm, StorageCondition,
    OrderStatus, PaymentMethod, PaymentStatus
)

class Medicine(TimestampMixin, SoftDeleteMixin, AuditMixin):
    """
    نموذج الأدوية
    """
    name = models.CharField(_('اسم الدواء'), max_length=200)
    scientific_name = models.CharField(_('الاسم العلمي'), max_length=200)
    category = models.CharField(
        _('الفئة'),
        max_length=20,
        choices=MedicineCategory.choices,
        default=MedicineCategory.OTHER
    )
    form = models.CharField(
        _('الشكل'),
        max_length=20,
        choices=MedicineForm.choices,
        default=MedicineForm.TABLET
    )
    manufacturer = models.CharField(_('الشركة المصنعة'), max_length=200)
    description = models.TextField(_('الوصف'))
    dosage = models.CharField(_('الجرعة'), max_length=100, null=True, blank=True)
    storage_condition = models.CharField(
        _('ظروف التخزين'),
        max_length=20,
        choices=StorageCondition.choices,
        default=StorageCondition.ROOM_TEMP
    )
    price = models.DecimalField(_('السعر'), max_digits=10, decimal_places=2)
    requires_prescription = models.BooleanField(_('يتطلب وصفة طبية'), default=True)
    is_available = models.BooleanField(_('متوفر'), default=True)
    image = models.ImageField(_('الصورة'), upload_to='medicines/', null=True, blank=True)
    barcode = models.CharField(_('الباركود'), max_length=50, unique=True, null=True, blank=True)
    expiry_date = models.DateField(_('تاريخ الصلاحية'), default=timezone.now)
    side_effects = models.TextField(_('الآثار الجانبية'), blank=True)
    contraindications = models.TextField(_('موانع الاستعمال'), blank=True)
    interactions = models.TextField(_('التفاعلات الدوائية'), blank=True)
    notes = models.TextField(_('ملاحظات'), blank=True)

    class Meta:
        verbose_name = _('دواء')
        verbose_name_plural = _('الأدوية')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.manufacturer})"

    @property
    def is_expired(self):
        """
        التحقق من انتهاء الصلاحية
        """
        return self.expiry_date <= timezone.now().date()

class Inventory(TimestampMixin, SoftDeleteMixin, AuditMixin):
    """
    نموذج المخزون
    """
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.PROTECT,
        related_name='inventory_records',
        verbose_name=_('الدواء')
    )
    batch_number = models.CharField(_('رقم التشغيلة'), max_length=50)
    quantity = models.PositiveIntegerField(_('الكمية'))
    unit_cost = models.DecimalField(_('تكلفة الوحدة'), max_digits=10, decimal_places=2)
    expiry_date = models.DateField(_('تاريخ الصلاحية'))
    supplier = models.CharField(_('المورد'), max_length=200)
    purchase_date = models.DateField(_('تاريخ الشراء'))
    notes = models.TextField(_('ملاحظات'), blank=True)

    class Meta:
        verbose_name = _('مخزون')
        verbose_name_plural = _('المخزون')
        ordering = ['expiry_date']
        unique_together = ['medicine', 'batch_number']

    def __str__(self):
        return f"{self.medicine.name} - {self.batch_number}"

    @property
    def total_cost(self):
        """
        حساب التكلفة الإجمالية
        """
        return self.quantity * self.unit_cost

class Order(TimestampMixin, SoftDeleteMixin, AuditMixin):
    """
    نموذج الطلبات
    """
    patient = models.ForeignKey(
        'accounts.User',
        on_delete=models.PROTECT,
        related_name='pharmacy_orders',
        limit_choices_to={'user_type': 'patient'},
        verbose_name=_('المريض')
    )
    prescription = models.ForeignKey(
        'medical_records.Prescription',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pharmacy_orders',
        verbose_name=_('الوصفة الطبية')
    )
    status = models.CharField(
        _('الحالة'),
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )
    payment_method = models.CharField(
        _('طريقة الدفع'),
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH
    )
    payment_status = models.CharField(
        _('حالة الدفع'),
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    delivery_address = models.TextField(_('عنوان التوصيل'), blank=True)
    delivery_notes = models.TextField(_('ملاحظات التوصيل'), blank=True)
    total_amount = models.DecimalField(_('المبلغ الإجمالي'), max_digits=10, decimal_places=2)
    discount = models.DecimalField(_('الخصم'), max_digits=10, decimal_places=2, default=0)
    insurance_coverage = models.DecimalField(
        _('تغطية التأمين'),
        max_digits=10,
        decimal_places=2,
        default=0
    )
    final_amount = models.DecimalField(_('المبلغ النهائي'), max_digits=10, decimal_places=2)
    notes = models.TextField(_('ملاحظات'), blank=True)

    class Meta:
        verbose_name = _('طلب')
        verbose_name_plural = _('الطلبات')
        ordering = ['-created_at']

    def __str__(self):
        return f"طلب {self.id} - {self.patient}"

    def save(self, *args, **kwargs):
        """
        حساب المبلغ النهائي
        """
        self.final_amount = self.total_amount - self.discount - self.insurance_coverage
        super().save(*args, **kwargs)

class OrderItem(TimestampMixin, AuditMixin):
    """
    نموذج عناصر الطلب
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('الطلب')
    )
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name=_('الدواء')
    )
    quantity = models.PositiveIntegerField(_('الكمية'))
    unit_price = models.DecimalField(_('سعر الوحدة'), max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(_('السعر الإجمالي'), max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(_('ملاحظات'), blank=True)

    class Meta:
        verbose_name = _('عنصر الطلب')
        verbose_name_plural = _('عناصر الطلب')
        ordering = ['id']

    def __str__(self):
        return f"{self.medicine.name} x {self.quantity}"

    def save(self, *args, **kwargs):
        """
        حساب السعر الإجمالي
        """
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

class StockAlert(TimestampMixin, AuditMixin):
    """
    نموذج تنبيهات المخزون
    """
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name='stock_alerts',
        verbose_name=_('الدواء')
    )
    min_quantity = models.PositiveIntegerField(_('الحد الأدنى للكمية'))
    current_quantity = models.PositiveIntegerField(_('الكمية الحالية'))
    is_resolved = models.BooleanField(_('تم الحل'), default=False)
    resolved_at = models.DateTimeField(_('تاريخ الحل'), null=True, blank=True)
    notes = models.TextField(_('ملاحظات'), blank=True)

    class Meta:
        verbose_name = _('تنبيه مخزون')
        verbose_name_plural = _('تنبيهات المخزون')
        ordering = ['-created_at']

    def __str__(self):
        return f"تنبيه مخزون - {self.medicine.name}"

    def resolve(self):
        """
        حل التنبيه
        """
        self.is_resolved = True
        self.resolved_at = timezone.now()
        self.save()

class ExpiryAlert(TimestampMixin, AuditMixin):
    """
    نموذج تنبيهات انتهاء الصلاحية
    """
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name='expiry_alerts',
        verbose_name=_('الدواء')
    )
    batch_number = models.CharField(_('رقم التشغيلة'), max_length=50)
    expiry_date = models.DateField(_('تاريخ الصلاحية'))
    quantity = models.PositiveIntegerField(_('الكمية'))
    is_resolved = models.BooleanField(_('تم الحل'), default=False)
    resolved_at = models.DateTimeField(_('تاريخ الحل'), null=True, blank=True)
    resolution_notes = models.TextField(_('ملاحظات الحل'), blank=True)

    class Meta:
        verbose_name = _('تنبيه صلاحية')
        verbose_name_plural = _('تنبيهات الصلاحية')
        ordering = ['expiry_date']

    def __str__(self):
        return f"تنبيه صلاحية - {self.medicine.name} ({self.batch_number})"

    def resolve(self, notes=''):
        """
        حل التنبيه
        """
        self.is_resolved = True
        self.resolved_at = timezone.now()
        self.resolution_notes = notes
        self.save()
