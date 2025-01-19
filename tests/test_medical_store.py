from datetime import date

import pytest
from django.test import Client

from medical_store.models import Inventory, MedicalEquipment, Medicine


@pytest.mark.django_db
class TestMedicalStore:
    @pytest.fixture
    def client(self):
        return Client()

    @pytest.fixture
    def test_medicine(self):
        return Medicine.objects.create(
            name="Test Medicine",
            generic_name="Test Generic",
            manufacturer="Test Manufacturer",
            price=10.00,
            prescription_required=True,
        )

    @pytest.fixture
    def test_equipment(self):
        return MedicalEquipment.objects.create(
            name="Test Equipment",
            manufacturer="Test Manufacturer",
            price=100.00,
            category="Diagnostic",
        )

    def test_add_medicine(self):
        medicine = Medicine.objects.create(
            name="Paracetamol",
            generic_name="Acetaminophen",
            manufacturer="Pharma Co",
            price=5.00,
            prescription_required=False,
        )
        assert medicine.name == "Paracetamol"
        assert not medicine.prescription_required

    def test_add_equipment(self):
        equipment = MedicalEquipment.objects.create(
            name="Stethoscope",
            manufacturer="Medical Co",
            price=50.00,
            category="Diagnostic",
        )
        assert equipment.name == "Stethoscope"
        assert equipment.category == "Diagnostic"

    def test_update_inventory(self, test_medicine):
        inventory = Inventory.objects.create(
            item=test_medicine, quantity=100, expiry_date=date(2026, 1, 1)
        )
        inventory.quantity = 90
        inventory.save()
        assert inventory.quantity == 90

    def test_check_low_stock(self, test_medicine):
        inventory = Inventory.objects.create(
            item=test_medicine, quantity=5, expiry_date=date(2026, 1, 1)
        )
        assert inventory.quantity <= 10  # Low stock threshold

    def test_check_expiry(self, test_medicine):
        inventory = Inventory.objects.create(
            item=test_medicine, quantity=100, expiry_date=date(2024, 1, 1)  # Past date
        )
        assert inventory.expiry_date < date.today()
