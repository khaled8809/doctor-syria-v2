from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from saas_core.models import Tenant, TenantUser

from ..models import (
    Admission,
    Department,
    Doctor,
    EmergencyCase,
    Hospital,
    Inventory,
    MedicalSupply,
    Patient,
    PurchaseOrder,
)

User = get_user_model()


class HospitalModelTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(
            name="مستشفى الأمل", subdomain="amal", is_active=True
        )
        self.hospital = Hospital.objects.create(
            tenant=self.tenant,
            name="مستشفى الأمل",
            address="دمشق، سوريا",
            phone="0911234567",
            email="info@amal-hospital.com",
            license_number="12345",
        )

    def test_hospital_creation(self):
        """اختبار إنشاء مستشفى جديد"""
        self.assertEqual(self.hospital.name, "مستشفى الأمل")
        self.assertEqual(self.hospital.tenant, self.tenant)
        self.assertTrue(self.hospital.is_active)

    def test_hospital_str_representation(self):
        """اختبار تمثيل المستشفى كنص"""
        self.assertEqual(str(self.hospital), "مستشفى الأمل")


class DepartmentModelTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="مستشفى الأمل", subdomain="amal")
        self.hospital = Hospital.objects.create(tenant=self.tenant, name="مستشفى الأمل")
        self.user = User.objects.create_user(username="doctor", password="testpass123")
        self.doctor = Doctor.objects.create(
            user=self.user, tenant=self.tenant, specialty="جراحة عامة"
        )
        self.department = Department.objects.create(
            hospital=self.hospital, name="قسم الجراحة", head_doctor=self.doctor
        )

    def test_department_creation(self):
        """اختبار إنشاء قسم جديد"""
        self.assertEqual(self.department.name, "قسم الجراحة")
        self.assertEqual(self.department.hospital, self.hospital)
        self.assertEqual(self.department.head_doctor, self.doctor)


class EmergencyCaseModelTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="مستشفى الأمل", subdomain="amal")
        self.hospital = Hospital.objects.create(tenant=self.tenant, name="مستشفى الأمل")
        self.patient = Patient.objects.create(
            tenant=self.tenant, first_name="أحمد", last_name="محمد", phone="0911234567"
        )
        self.emergency = EmergencyCase.objects.create(
            tenant=self.tenant,
            patient=self.patient,
            hospital=self.hospital,
            condition="حالة طارئة",
            priority="عالية",
        )

    def test_emergency_case_creation(self):
        """اختبار إنشاء حالة طوارئ جديدة"""
        self.assertEqual(self.emergency.patient, self.patient)
        self.assertEqual(self.emergency.hospital, self.hospital)
        self.assertEqual(self.emergency.priority, "عالية")
        self.assertIsNotNone(self.emergency.created_at)

    def test_emergency_case_status_update(self):
        """اختبار تحديث حالة الطوارئ"""
        self.emergency.status = "معالجة"
        self.emergency.save()
        self.assertEqual(self.emergency.status, "معالجة")


class InventoryModelTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="مستشفى الأمل", subdomain="amal")
        self.supply = MedicalSupply.objects.create(
            tenant=self.tenant, name="قفازات طبية", code="GLV001", unit="علبة"
        )
        self.inventory = Inventory.objects.create(
            tenant=self.tenant, supply=self.supply, quantity=100, minimum_quantity=20
        )

    def test_inventory_creation(self):
        """اختبار إنشاء مخزون جديد"""
        self.assertEqual(self.inventory.supply, self.supply)
        self.assertEqual(self.inventory.quantity, 100)
        self.assertEqual(self.inventory.minimum_quantity, 20)

    def test_low_stock_alert(self):
        """اختبار تنبيه المخزون المنخفض"""
        self.inventory.quantity = 15
        self.inventory.save()
        self.assertTrue(self.inventory.is_low_stock())


class PurchaseOrderModelTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="مستشفى الأمل", subdomain="amal")
        self.supply = MedicalSupply.objects.create(
            tenant=self.tenant, name="قفازات طبية", code="GLV001"
        )
        self.purchase_order = PurchaseOrder.objects.create(
            tenant=self.tenant, order_number="PO001", status="جديد"
        )

    def test_purchase_order_creation(self):
        """اختبار إنشاء طلب شراء جديد"""
        self.assertEqual(self.purchase_order.order_number, "PO001")
        self.assertEqual(self.purchase_order.status, "جديد")
        self.assertIsNotNone(self.purchase_order.created_at)

    def test_purchase_order_status_update(self):
        """اختبار تحديث حالة طلب الشراء"""
        self.purchase_order.status = "مكتمل"
        self.purchase_order.save()
        self.assertEqual(self.purchase_order.status, "مكتمل")
