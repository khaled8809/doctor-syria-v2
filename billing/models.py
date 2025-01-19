import uuid
from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from patient_records.models import Patient


class Invoice(models.Model):
    """نموذج الفاتورة"""

    STATUS_CHOICES = [
        ("draft", "مسودة"),
        ("pending", "معلق"),
        ("paid", "مدفوع"),
        ("cancelled", "ملغي"),
        ("refunded", "مسترد"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("cash", "نقداً"),
        ("card", "بطاقة ائتمان"),
        ("bank_transfer", "تحويل بنكي"),
        ("insurance", "تأمين"),
    ]

    invoice_number = models.CharField(
        max_length=50,
        unique=True,
        default=lambda: f"INV-{uuid.uuid4().hex[:8].upper()}",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="invoices",
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="doctor_invoices",
    )
    appointment = models.OneToOneField(
        "appointments.Appointment",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="invoice",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True
    )
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    tax = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    total = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField()
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["invoice_number"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.invoice_number} - {self.patient.user.get_full_name()}"

    def calculate_total(self):
        """حساب المجموع الكلي للفاتورة"""
        self.total = self.subtotal + self.tax - self.discount
        return self.total

    def mark_as_paid(self, payment_method):
        """تحديث حالة الفاتورة إلى مدفوعة"""
        self.status = "paid"
        self.payment_method = payment_method
        self.paid_at = timezone.now()
        self.save()


class InvoiceItem(models.Model):
    """نموذج عنصر الفاتورة"""

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )

    def save(self, *args, **kwargs):
        """حساب السعر الإجمالي للعنصر"""
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class Payment(models.Model):
    """نموذج الدفع"""

    STATUS_CHOICES = [
        ("pending", "معلق"),
        ("completed", "مكتمل"),
        ("failed", "فشل"),
        ("refunded", "مسترد"),
    ]

    invoice = models.ForeignKey(
        Invoice, on_delete=models.PROTECT, related_name="payments"
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    payment_method = models.CharField(
        max_length=20, choices=Invoice.PAYMENT_METHOD_CHOICES
    )
    transaction_id = models.CharField(
        max_length=100, unique=True, null=True, blank=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Payment {self.id} for Invoice {self.invoice.invoice_number}"


class InsuranceClaim(models.Model):
    """نموذج مطالبة التأمين"""

    STATUS_CHOICES = [
        ("pending", "معلق"),
        ("approved", "موافق عليه"),
        ("rejected", "مرفوض"),
        ("paid", "مدفوع"),
    ]

    invoice = models.OneToOneField(
        Invoice, on_delete=models.PROTECT, related_name="insurance_claim"
    )
    insurance_provider = models.ForeignKey(
        "InsuranceProvider", on_delete=models.PROTECT, related_name="claims"
    )
    claim_number = models.CharField(
        max_length=50,
        unique=True,
        default=lambda: f"CLM-{uuid.uuid4().hex[:8].upper()}",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    amount_claimed = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    amount_approved = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"Claim {self.claim_number} for Invoice {self.invoice.invoice_number}"


class InsuranceProvider(models.Model):
    """نموذج شركة التأمين"""

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class StripePayment(models.Model):
    """نموذج مدفوعات Stripe"""

    payment = models.OneToOneField(
        Payment, on_delete=models.CASCADE, related_name="stripe_payment"
    )
    stripe_charge_id = models.CharField(max_length=100, unique=True)
    stripe_payment_intent_id = models.CharField(max_length=100, unique=True)
    card_last4 = models.CharField(max_length=4)
    card_brand = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Stripe payment for {self.payment.invoice.invoice_number}"


class FaturaPayment(models.Model):
    """نموذج مدفوعات Fatura"""

    payment = models.OneToOneField(
        Payment, on_delete=models.CASCADE, related_name="fatura_payment"
    )
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_url = models.URLField()
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    payment_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "قيد الانتظار"),
            ("completed", "مكتمل"),
            ("failed", "فشل"),
            ("refunded", "مسترد"),
        ],
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Fatura payment for {self.payment.invoice.invoice_number}"
