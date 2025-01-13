from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from billing.models import InsuranceClaim, Invoice, Payment
from patient_records.models import Patient

User = get_user_model()


@pytest.mark.django_db
class TestBilling:
    @pytest.fixture
    def client(self):
        return Client()

    @pytest.fixture
    def test_user(self):
        return User.objects.create_user(
            username="testpatient", email="patient@test.com", password="testpass123"
        )

    @pytest.fixture
    def test_patient(self, test_user):
        return Patient.objects.create(user=test_user, date_of_birth="1990-01-01")

    def test_create_invoice(self, test_patient):
        invoice = Invoice.objects.create(
            patient=test_patient,
            amount=Decimal("100.00"),
            description="Consultation Fee",
        )
        assert invoice.amount == Decimal("100.00")
        assert invoice.status == "pending"

    def test_process_payment(self, test_patient):
        invoice = Invoice.objects.create(
            patient=test_patient,
            amount=Decimal("100.00"),
            description="Consultation Fee",
        )
        payment = Payment.objects.create(
            invoice=invoice, amount=Decimal("100.00"), payment_method="credit_card"
        )
        invoice.status = "paid"
        invoice.save()
        assert payment.amount == invoice.amount
        assert invoice.status == "paid"

    def test_partial_payment(self, test_patient):
        invoice = Invoice.objects.create(
            patient=test_patient,
            amount=Decimal("100.00"),
            description="Consultation Fee",
        )
        payment = Payment.objects.create(
            invoice=invoice, amount=Decimal("50.00"), payment_method="cash"
        )
        assert invoice.amount - payment.amount == Decimal("50.00")
        assert invoice.status == "pending"

    def test_insurance_claim(self, test_patient):
        invoice = Invoice.objects.create(
            patient=test_patient, amount=Decimal("1000.00"), description="Surgery"
        )
        claim = InsuranceClaim.objects.create(
            invoice=invoice,
            insurance_provider="Test Insurance",
            claim_amount=Decimal("800.00"),
            status="submitted",
        )
        assert claim.claim_amount == Decimal("800.00")
        assert claim.status == "submitted"

    def test_invoice_validation(self, test_patient):
        with pytest.raises(ValueError):
            Invoice.objects.create(
                patient=test_patient, amount=Decimal("-100.00")  # Negative amount
            )
