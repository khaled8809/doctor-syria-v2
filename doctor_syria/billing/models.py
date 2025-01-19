from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from accounts.models import Hospital, Patient


class ServiceCategory(models.Model):
    """فئات الخدمات"""

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Service Categories"


class Service(models.Model):
    """الخدمات"""

    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    duration = models.DurationField(null=True, blank=True)
    requires_approval = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code} - {self.name}"


class PriceList(models.Model):
    """قوائم الأسعار"""

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.hospital.name}"


class PriceListItem(models.Model):
    """عناصر قائمة الأسعار"""

    price_list = models.ForeignKey(PriceList, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return f"{self.service.name} - {self.price}"


class Invoice(models.Model):
    """الفواتير"""

    STATUS_CHOICES = [
        ("draft", "مسودة"),
        ("issued", "صادرة"),
        ("paid", "مدفوعة"),
        ("partially_paid", "مدفوعة جزئياً"),
        ("overdue", "متأخرة"),
        ("cancelled", "ملغية"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"فاتورة {self.invoice_number}"


class InvoiceItem(models.Model):
    """عناصر الفاتورة"""

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.service.name} - {self.quantity}"


class Payment(models.Model):
    """المدفوعات"""

    PAYMENT_METHODS = [
        ("cash", "نقدي"),
        ("credit_card", "بطاقة ائتمان"),
        ("debit_card", "بطاقة خصم"),
        ("bank_transfer", "تحويل بنكي"),
        ("insurance", "تأمين"),
        ("other", "أخرى"),
    ]

    STATUS_CHOICES = [
        ("pending", "قيد الانتظار"),
        ("completed", "مكتمل"),
        ("failed", "فشل"),
        ("refunded", "مسترد"),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_date = models.DateTimeField(default=timezone.now)
    transaction_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"دفعة {self.amount} - {self.get_payment_method_display()}"


class InsuranceClaim(models.Model):
    """مطالبات التأمين"""

    STATUS_CHOICES = [
        ("submitted", "مقدمة"),
        ("in_review", "قيد المراجعة"),
        ("approved", "موافق عليها"),
        ("partially_approved", "موافق عليها جزئياً"),
        ("rejected", "مرفوضة"),
        ("paid", "مدفوعة"),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    insurance_provider = models.ForeignKey(
        "insurance.InsuranceProvider", on_delete=models.CASCADE
    )
    claim_number = models.CharField(max_length=100, unique=True)
    submission_date = models.DateField()
    amount_claimed = models.DecimalField(max_digits=10, decimal_places=2)
    amount_approved = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="submitted")
    rejection_reason = models.TextField(blank=True)
    documents = models.JSONField(default=list)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"مطالبة {self.claim_number}"


class Refund(models.Model):
    """المبالغ المستردة"""

    STATUS_CHOICES = [
        ("pending", "قيد الانتظار"),
        ("approved", "موافق عليه"),
        ("rejected", "مرفوض"),
        ("processed", "تمت المعالجة"),
    ]

    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    requested_by = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="refund_requests"
    )
    approved_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="refund_approvals",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    request_date = models.DateTimeField(auto_now_add=True)
    process_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"استرداد {self.amount} - {self.payment}"
