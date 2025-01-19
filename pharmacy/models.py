"""
نماذج تطبيق الصيدلية
"""

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from patient_records.models import Patient


class Medicine(models.Model):
    """نموذج الدواء"""

    name = models.CharField(_("اسم الدواء"), max_length=255)
    scientific_name = models.CharField(_("الاسم العلمي"), max_length=255)
    manufacturer = models.CharField(_("الشركة المصنعة"), max_length=255)
    description = models.TextField(_("الوصف"))
    dosage_form = models.CharField(_("شكل الجرعة"), max_length=100)
    strength = models.CharField(_("التركيز"), max_length=100)
    price = models.DecimalField(_("السعر"), max_digits=10, decimal_places=2)
    requires_prescription = models.BooleanField(_("يتطلب وصفة طبية"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("دواء")
        verbose_name_plural = _("الأدوية")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.strength})"


class Inventory(models.Model):
    """نموذج المخزون"""

    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name="inventory_items",
        verbose_name=_("الدواء"),
    )
    batch_number = models.CharField(_("رقم التشغيلة"), max_length=100)
    expiry_date = models.DateField(_("تاريخ انتهاء الصلاحية"))
    quantity = models.PositiveIntegerField(
        _("الكمية"),
        validators=[MinValueValidator(0)],
    )
    reorder_level = models.PositiveIntegerField(_("مستوى إعادة الطلب"), default=10)
    unit_cost = models.DecimalField(_("تكلفة الوحدة"), max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("مخزون")
        verbose_name_plural = _("المخزون")
        ordering = ["medicine__name", "expiry_date"]

    def __str__(self):
        return f"{self.medicine} - {self.batch_number}"

    def is_low_stock(self):
        """التحقق من المخزون المنخفض"""
        return self.quantity <= self.reorder_level


class InventoryTransaction(models.Model):
    """نموذج حركات المخزون"""

    TRANSACTION_TYPES = [
        ("purchase", _("شراء")),
        ("sale", _("بيع")),
        ("return", _("مرتجع")),
        ("adjustment", _("تسوية")),
        ("expired", _("منتهي الصلاحية")),
    ]

    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name=_("المخزون"),
    )
    transaction_type = models.CharField(
        _("نوع الحركة"),
        max_length=20,
        choices=TRANSACTION_TYPES,
    )
    quantity = models.IntegerField(_("الكمية"))
    unit_price = models.DecimalField(
        _("سعر الوحدة"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    reference = models.CharField(
        _("المرجع"),
        max_length=100,
        help_text=_("رقم الفاتورة أو رقم المرجع"),
    )
    notes = models.TextField(_("ملاحظات"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pharmacy_transactions'
    )

    class Meta:
        verbose_name = _("حركة مخزون")
        verbose_name_plural = _("حركات المخزون")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.inventory} - {self.get_transaction_type_display()} - {self.quantity}"

    def save(self, *args, **kwargs):
        """تحديث كمية المخزون"""
        if self.transaction_type in ["purchase", "return"]:
            self.inventory.quantity += self.quantity
        else:
            self.inventory.quantity -= self.quantity
        self.inventory.save()
        super().save(*args, **kwargs)


class Prescription(models.Model):
    """نموذج الوصفة الطبية"""

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="pharmacy_prescriptions",
        verbose_name=_("المريض"),
    )
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pharmacy_prescriptions",
        verbose_name=_("الطبيب"),
    )
    diagnosis = models.TextField(_("التشخيص"))
    notes = models.TextField(_("الملاحظات"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(_("فعال"), default=True)

    class Meta:
        verbose_name = _("وصفة طبية")
        verbose_name_plural = _("الوصفات الطبية")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.patient} - {self.created_at}"


class PrescriptionItem(models.Model):
    """نموذج عنصر الوصفة الطبية"""

    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("الوصفة الطبية"),
    )
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.PROTECT,
        related_name="prescription_items",
        verbose_name=_("الدواء"),
    )
    quantity = models.PositiveIntegerField(_("الكمية"))
    dosage = models.CharField(_("الجرعة"), max_length=100)
    frequency = models.CharField(_("التكرار"), max_length=100)
    duration = models.CharField(_("المدة"), max_length=100)
    instructions = models.TextField(_("التعليمات"))

    class Meta:
        verbose_name = _("عنصر الوصفة")
        verbose_name_plural = _("عناصر الوصفة")
        ordering = ["prescription", "id"]

    def __str__(self):
        return f"{self.medicine} - {self.quantity}"


class Sale(models.Model):
    """نموذج المبيعات"""

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="pharmacy_sales",
        verbose_name=_("المريض"),
    )
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sales",
        verbose_name=_("الوصفة الطبية"),
    )
    total_amount = models.DecimalField(_("المبلغ الإجمالي"), max_digits=10, decimal_places=2)
    payment_method = models.CharField(_("طريقة الدفع"), max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("عملية بيع")
        verbose_name_plural = _("عمليات البيع")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.patient} - {self.created_at}"


class SaleItem(models.Model):
    """نموذج عنصر المبيعات"""

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("عملية البيع"),
    )
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.PROTECT,
        related_name="sale_items",
        verbose_name=_("الدواء"),
    )
    quantity = models.PositiveIntegerField(_("الكمية"))
    unit_price = models.DecimalField(_("سعر الوحدة"), max_digits=10, decimal_places=2)
    total_price = models.DecimalField(_("السعر الإجمالي"), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _("عنصر البيع")
        verbose_name_plural = _("عناصر البيع")
        ordering = ["sale", "id"]

    def __str__(self):
        return f"{self.medicine} - {self.quantity}"

    def save(self, *args, **kwargs):
        """حساب السعر الإجمالي"""
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
