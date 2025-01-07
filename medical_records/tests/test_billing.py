from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from medical_records.models import (
    Invoice,
    InvoiceItem,
    Payment,
    Insurance,
    InsuranceClaim
)

User = get_user_model()

class BillingTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testpatient',
            password='testpass123',
            first_name='Test',
            last_name='Patient'
        )
        
        # Create an insurance policy
        self.insurance = Insurance.objects.create(
            patient=self.user,
            provider='Test Insurance Co',
            policy_number='TEST-001',
            coverage_type='full',
            coverage_percentage=80,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=365),
            status='active',
            deductible=Decimal('100.00'),
            max_coverage=Decimal('10000.00')
        )
        
        # Create an invoice
        self.invoice = Invoice.objects.create(
            patient=self.user,
            invoice_number='INV-001',
            status='pending',
            issue_date=timezone.now().date(),
            due_date=timezone.now().date() + timezone.timedelta(days=30),
            payment_method='cash',
            subtotal=Decimal('1000.00'),
            tax=Decimal('50.00'),
            discount=Decimal('100.00'),
            total=Decimal('950.00')
        )
        
        # Create an invoice item
        self.invoice_item = InvoiceItem.objects.create(
            invoice=self.invoice,
            description='Medical Consultation',
            quantity=1,
            unit_price=Decimal('1000.00'),
            total=Decimal('1000.00')
        )

    def test_invoice_creation(self):
        """Test invoice creation and total calculation"""
        self.assertEqual(self.invoice.total, Decimal('950.00'))
        self.assertEqual(self.invoice.status, 'pending')
        self.assertEqual(str(self.invoice), f"Invoice #{self.invoice.invoice_number} - {self.user}")

    def test_invoice_item_creation(self):
        """Test invoice item creation and total calculation"""
        self.assertEqual(self.invoice_item.total, Decimal('1000.00'))
        self.assertEqual(str(self.invoice_item), f"Medical Consultation - {self.invoice.invoice_number}")

    def test_payment_creation(self):
        """Test payment creation and processing"""
        payment = Payment.objects.create(
            invoice=self.invoice,
            amount=Decimal('950.00'),
            payment_method='cash',
            status='completed',
            payment_date=timezone.now()
        )
        self.assertEqual(payment.amount, Decimal('950.00'))
        self.assertEqual(payment.status, 'completed')

    def test_insurance_coverage(self):
        """Test insurance coverage calculation"""
        coverage = self.insurance.calculate_coverage(Decimal('1000.00'))
        expected_coverage = Decimal('800.00')  # 80% of 1000
        self.assertEqual(coverage, expected_coverage)

    def test_insurance_claim_creation(self):
        """Test insurance claim creation and processing"""
        claim = InsuranceClaim.objects.create(
            insurance=self.insurance,
            invoice=self.invoice,
            claim_number='CLM-001',
            submission_date=timezone.now().date(),
            status='submitted',
            amount_claimed=Decimal('800.00')
        )
        self.assertEqual(claim.status, 'submitted')
        self.assertEqual(claim.amount_claimed, Decimal('800.00'))
        
        # Test claim approval
        claim.status = 'approved'
        claim.amount_approved = Decimal('800.00')
        claim.save()
        self.assertTrue(claim.is_approved())
        self.assertEqual(claim.amount_approved, Decimal('800.00'))

    def test_insurance_active_status(self):
        """Test insurance active status check"""
        self.assertTrue(self.insurance.is_active())
        
        # Test expired insurance
        self.insurance.end_date = timezone.now().date() - timezone.timedelta(days=1)
        self.insurance.save()
        self.assertFalse(self.insurance.is_active())

    def test_invoice_overdue(self):
        """Test invoice overdue status"""
        self.assertFalse(self.invoice.is_overdue())
        
        # Set due date to yesterday
        self.invoice.due_date = timezone.now().date() - timezone.timedelta(days=1)
        self.invoice.save()
        self.assertTrue(self.invoice.is_overdue())
