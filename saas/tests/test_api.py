from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from saas_core.models import Tenant, TenantUser

from ..models import Department, Doctor, EmergencyCase, Hospital, MedicalSupply, Patient

User = get_user_model()


class BaseAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # إنشاء مستخدم للاختبار
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", email="test@example.com"
        )
        # إنشاء مستأجر للاختبار
        self.tenant = Tenant.objects.create(
            name="مستشفى الاختبار", subdomain="test", is_active=True
        )
        # ربط المستخدم بالمستأجر
        self.tenant_user = TenantUser.objects.create(
            user=self.user, tenant=self.tenant, role="admin"
        )
        # تسجيل دخول المستخدم
        self.client.force_authenticate(user=self.user)


class HospitalAPITest(BaseAPITest):
    def setUp(self):
        super().setUp()
        self.hospital = Hospital.objects.create(
            tenant=self.tenant,
            name="مستشفى الاختبار",
            address="دمشق، سوريا",
            phone="0911234567",
        )
        self.url = reverse("hospital-list")

    def test_get_hospitals_list(self):
        """اختبار الحصول على قائمة المستشفيات"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_create_hospital(self):
        """اختبار إنشاء مستشفى جديد"""
        data = {
            "name": "مستشفى جديد",
            "address": "حلب، سوريا",
            "phone": "0921234567",
            "email": "info@new-hospital.com",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Hospital.objects.count(), 2)


class EmergencyCaseAPITest(BaseAPITest):
    def setUp(self):
        super().setUp()
        self.hospital = Hospital.objects.create(
            tenant=self.tenant, name="مستشفى الاختبار"
        )
        self.patient = Patient.objects.create(
            tenant=self.tenant, first_name="أحمد", last_name="محمد"
        )
        self.emergency = EmergencyCase.objects.create(
            tenant=self.tenant,
            patient=self.patient,
            hospital=self.hospital,
            condition="حالة طارئة",
            priority="عالية",
        )
        self.url = reverse("emergencycase-list")

    def test_get_emergency_cases(self):
        """اختبار الحصول على قائمة حالات الطوارئ"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_create_emergency_case(self):
        """اختبار إنشاء حالة طوارئ جديدة"""
        data = {
            "patient": self.patient.id,
            "hospital": self.hospital.id,
            "condition": "كسر في الساق",
            "priority": "متوسطة",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EmergencyCase.objects.count(), 2)


class MedicalSupplyAPITest(BaseAPITest):
    def setUp(self):
        super().setUp()
        self.supply = MedicalSupply.objects.create(
            tenant=self.tenant, name="قفازات طبية", code="GLV001", unit="علبة"
        )
        self.url = reverse("medicalsupply-list")

    def test_get_supplies(self):
        """اختبار الحصول على قائمة المستلزمات الطبية"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_create_supply(self):
        """اختبار إنشاء مستلزم طبي جديد"""
        data = {
            "name": "كمامات طبية",
            "code": "MSK001",
            "unit": "علبة",
            "description": "كمامات طبية عالية الجودة",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MedicalSupply.objects.count(), 2)

    def test_update_supply(self):
        """اختبار تحديث بيانات مستلزم طبي"""
        url = reverse("medicalsupply-detail", args=[self.supply.id])
        data = {"name": "قفازات طبية معقمة", "code": "GLV001", "unit": "علبة"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.supply.refresh_from_db()
        self.assertEqual(self.supply.name, "قفازات طبية معقمة")
