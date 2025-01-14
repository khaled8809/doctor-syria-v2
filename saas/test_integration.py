from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from saas_core.models import Tenant, TenantUser

from .models import (
    Admission,
    Department,
    Doctor,
    EmergencyCase,
    Hospital,
    InventoryItem,
    MedicalCompany,
    MedicalSupply,
    Patient,
    PurchaseOrder,
    PurchaseOrderItem,
    Warehouse,
)

User = get_user_model()


class EmergencyAdmissionFlowTest(APITestCase):
    def setUp(self):
        """إعداد بيانات الاختبار"""
        self.client = APIClient()
        self.tenant = Tenant.objects.create(
            name="مستشفى الاختبار", subdomain="test", is_active=True
        )
        self.hospital = Hospital.objects.create(
            tenant=self.tenant,
            name="مستشفى الاختبار",
            code="TEST001",
            city="دمشق",
            address="شارع الاختبار",
            phone="0911234567",
            bed_capacity=100,
            available_beds=50,
        )
        self.user = User.objects.create_user(
            username="doctor",
            password="testpass123",
            first_name="طبيب",
            last_name="اختبار",
        )
        self.doctor = Doctor.objects.create(
            tenant=self.tenant,
            user=self.user,
            specialization="طوارئ",
            license_number="LIC001",
            phone="0911234567",
        )
        self.department = Department.objects.create(
            hospital=self.hospital,
            name="قسم الطوارئ",
            specialty="طوارئ",
            head_doctor=self.doctor,
            capacity=20,
            available_beds=10,
            floor="1",
            phone_extension="101",
        )
        self.patient = Patient.objects.create(
            tenant=self.tenant,
            name="أحمد محمد",
            age=30,
            gender="ذكر",
            condition="حالة مستقرة",
        )
        self.client.force_authenticate(user=self.user)

    def test_complete_emergency_flow(self):
        """اختبار السيناريو الكامل لحالة طوارئ"""
        # 1. إنشاء حالة طوارئ
        emergency_data = {
            "patient": self.patient.id,
            "hospital": self.hospital.id,
            "arrival_date": timezone.now().isoformat(),
            "condition": "إصابة خطيرة",
            "priority": "CRITICAL",
            "attending_doctor": self.doctor.id,
            "initial_diagnosis": "كسر في الساق",
            "treatment": "تجبير وعلاج",
            "notes": "حالة تحتاج لمتابعة",
        }
        response = self.client.post(reverse("emergencycase-list"), emergency_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        emergency_id = response.data["id"]

        # 2. إنشاء سجل دخول للمريض
        admission_data = {
            "patient": self.patient.id,
            "hospital": self.hospital.id,
            "department": self.department.id,
            "doctor": self.doctor.id,
            "admission_date": timezone.now().isoformat(),
            "reason": "إصابة خطيرة تحتاج للعلاج",
            "diagnosis": "كسر في الساق",
            "treatment_plan": "تجبير وعلاج طبيعي",
            "room_number": "E101",
            "bed_number": "B1",
            "status": "ADMITTED",
        }
        response = self.client.post(reverse("admission-list"), admission_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        admission_id = response.data["id"]

        # 3. تحديث حالة الطوارئ
        emergency_update = {"outcome": "ADMITTED"}
        response = self.client.patch(
            reverse("emergencycase-detail", args=[emergency_id]), emergency_update
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 4. تحديث سجل الدخول عند الخروج
        admission_complete = {
            "status": "DISCHARGED",
            "discharge_date": timezone.now().isoformat(),
        }
        response = self.client.patch(
            reverse("admission-detail", args=[admission_id]), admission_complete
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class InventoryManagementFlowTest(APITestCase):
    def setUp(self):
        """إعداد بيانات الاختبار"""
        self.client = APIClient()
        self.tenant = Tenant.objects.create(
            name="مستشفى الاختبار", subdomain="test", is_active=True
        )
        self.hospital = Hospital.objects.create(
            tenant=self.tenant,
            name="مستشفى الاختبار",
            code="TEST001",
            city="دمشق",
            address="شارع الاختبار",
            phone="0911234567",
            bed_capacity=100,
            available_beds=50,
        )
        self.user = User.objects.create_user(
            username="manager",
            password="testpass123",
            first_name="مدير",
            last_name="المخزون",
            is_staff=True,
        )
        self.tenant_user = TenantUser.objects.create(
            user=self.user, tenant=self.tenant, role="admin"
        )
        self.company = MedicalCompany.objects.create(
            tenant=self.tenant,
            name="شركة الأدوية",
            license_number="MED001",
            contact_person="محمد أحمد",
            email="contact@med.com",
            phone="0921234567",
            address="دمشق",
            registration_date=timezone.now().date(),
        )
        self.warehouse = Warehouse.objects.create(
            tenant=self.tenant,
            name="المستودع الرئيسي",
            warehouse_type="MEDICAL_SUPPLIES",
            location="دمشق",
            capacity=1000,
            temperature=20,
            humidity=50,
            manager=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_complete_inventory_flow(self):
        """اختبار السيناريو الكامل لإدارة المخزون"""
        # 1. إنشاء مستلزم طبي
        supply_data = {
            "tenant": self.tenant.id,
            "name": "قفازات طبية",
            "code": "GLV001",
            "supply_type": "DISPOSABLE",
            "manufacturer": self.company.id,
            "description": "قفازات طبية للاستخدام مرة واحدة",
            "unit": "علبة",
            "minimum_quantity": 20,
            "storage_condition": "NORMAL",
        }
        response = self.client.post(reverse("medicalsupply-list"), supply_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        supply_id = response.data["id"]

        # 2. إنشاء عنصر مخزون
        inventory_data = {
            "tenant": self.tenant.id,
            "supply": supply_id,
            "warehouse": self.warehouse.id,
            "batch_number": "BATCH001",
            "quantity": 100,
            "unit_price": 10.0,
            "manufacturing_date": timezone.now().date().isoformat(),
            "expiry_date": (
                timezone.now().date() + timezone.timedelta(days=365)
            ).isoformat(),
            "location_in_warehouse": "A1-B1-C1",
        }
        response = self.client.post(reverse("inventoryitem-list"), inventory_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        inventory_id = response.data["id"]

        # 3. إنشاء طلب شراء
        order_data = {
            "tenant": self.tenant.id,
            "order_number": "PO001",
            "supplier": self.company.id,
            "warehouse": self.warehouse.id,
            "status": "DRAFT",
            "expected_delivery_date": (
                timezone.now().date() + timezone.timedelta(days=7)
            ).isoformat(),
            "total_amount": 500.0,
            "created_by": self.user.id,
        }
        response = self.client.post(reverse("purchaseorder-list"), order_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order_id = response.data["id"]

        # 4. إضافة عناصر لطلب الشراء
        item_data = {
            "purchase_order": order_id,
            "supply": supply_id,
            "quantity": 50,
            "unit_price": 10.0,
        }
        response = self.client.post(reverse("purchaseorderitem-list"), item_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 5. تحديث حالة الطلب
        order_update = {"status": "RECEIVED"}
        response = self.client.patch(
            reverse("purchaseorder-detail", args=[order_id]), order_update
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 6. تحديث المخزون
        inventory_update = {"quantity": 150}  # 100 + 50
        response = self.client.patch(
            reverse("inventoryitem-detail", args=[inventory_id]), inventory_update
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
