from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

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
    PurchaseOrderItem,
)

User = get_user_model()


class EmergencyAdmissionScenarioTest(TestCase):
    def setUp(self):
        # إعداد البيانات الأساسية
        self.tenant = Tenant.objects.create(name="مستشفى الاختبار", subdomain="test")
        self.hospital = Hospital.objects.create(
            tenant=self.tenant, name="مستشفى الاختبار"
        )
        self.user = User.objects.create_user(username="doctor", password="testpass123")
        self.doctor = Doctor.objects.create(
            user=self.user, tenant=self.tenant, specialty="طوارئ"
        )
        self.department = Department.objects.create(
            hospital=self.hospital, name="قسم الطوارئ", head_doctor=self.doctor
        )
        self.patient = Patient.objects.create(
            tenant=self.tenant, first_name="أحمد", last_name="محمد", phone="0911234567"
        )

    def test_emergency_admission_flow(self):
        """اختبار سيناريو دخول حالة طارئة"""
        # 1. إنشاء حالة طوارئ
        emergency = EmergencyCase.objects.create(
            tenant=self.tenant,
            patient=self.patient,
            hospital=self.hospital,
            condition="إصابة خطيرة",
            priority="عالية",
        )
        self.assertEqual(emergency.status, "جديد")

        # 2. تحويل الحالة إلى قسم الطوارئ
        admission = Admission.objects.create(
            tenant=self.tenant,
            patient=self.patient,
            hospital=self.hospital,
            department=self.department,
            doctor=self.doctor,
            admission_type="طوارئ",
            emergency_case=emergency,
        )
        self.assertEqual(admission.status, "نشط")

        # 3. تحديث حالة الطوارئ
        emergency.status = "قيد المعالجة"
        emergency.save()
        self.assertEqual(emergency.status, "قيد المعالجة")

        # 4. إنهاء الحالة
        emergency.status = "مكتمل"
        emergency.save()
        admission.status = "مغادر"
        admission.discharge_date = timezone.now()
        admission.save()

        self.assertEqual(emergency.status, "مكتمل")
        self.assertEqual(admission.status, "مغادر")
        self.assertIsNotNone(admission.discharge_date)


class InventoryManagementScenarioTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="مستشفى الاختبار", subdomain="test")
        self.hospital = Hospital.objects.create(
            tenant=self.tenant, name="مستشفى الاختبار"
        )
        # إنشاء مستلزمات طبية
        self.supply1 = MedicalSupply.objects.create(
            tenant=self.tenant, name="قفازات طبية", code="GLV001", unit="علبة"
        )
        self.supply2 = MedicalSupply.objects.create(
            tenant=self.tenant, name="محاقن", code="SYR001", unit="علبة"
        )
        # إنشاء مخزون
        self.inventory1 = Inventory.objects.create(
            tenant=self.tenant, supply=self.supply1, quantity=100, minimum_quantity=20
        )
        self.inventory2 = Inventory.objects.create(
            tenant=self.tenant, supply=self.supply2, quantity=50, minimum_quantity=10
        )

    def test_purchase_order_flow(self):
        """اختبار سيناريو طلب شراء وتحديث المخزون"""
        # 1. إنشاء طلب شراء
        purchase_order = PurchaseOrder.objects.create(
            tenant=self.tenant, order_number="PO001", status="جديد"
        )

        # 2. إضافة عناصر لطلب الشراء
        item1 = PurchaseOrderItem.objects.create(
            purchase_order=purchase_order,
            supply=self.supply1,
            quantity=50,
            unit_price=10.0,
        )
        item2 = PurchaseOrderItem.objects.create(
            purchase_order=purchase_order,
            supply=self.supply2,
            quantity=30,
            unit_price=5.0,
        )

        # 3. تحديث حالة الطلب إلى مكتمل
        purchase_order.status = "مكتمل"
        purchase_order.save()

        # 4. تحديث المخزون
        self.inventory1.quantity += item1.quantity
        self.inventory1.save()
        self.inventory2.quantity += item2.quantity
        self.inventory2.save()

        # 5. التحقق من صحة التحديثات
        self.assertEqual(purchase_order.status, "مكتمل")
        self.assertEqual(self.inventory1.quantity, 150)  # 100 + 50
        self.assertEqual(self.inventory2.quantity, 80)  # 50 + 30

    def test_low_stock_alert(self):
        """اختبار تنبيهات المخزون المنخفض"""
        # تخفيض كمية المخزون
        self.inventory1.quantity = 15  # أقل من الحد الأدنى (20)
        self.inventory1.save()

        # التحقق من حالة المخزون
        self.assertTrue(self.inventory1.is_low_stock())
        self.assertFalse(self.inventory2.is_low_stock())
