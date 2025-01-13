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
    Inventory,
    MedicalSupply,
    Patient,
    PurchaseOrder,
    PurchaseOrderItem,
)

User = get_user_model()


class HospitalModelTest(TestCase):
    def setUp(self):
        """إعداد بيانات الاختبار"""
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

    def test_hospital_str(self):
        """اختبار تمثيل المستشفى كنص"""
        self.assertEqual(str(self.hospital), "مستشفى الأمل")


class DepartmentModelTest(TestCase):
    def setUp(self):
        """إعداد بيانات الاختبار"""
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


class HospitalAPITest(APITestCase):
    def setUp(self):
        """إعداد بيانات الاختبار"""
        self.client = APIClient()
        self.tenant = Tenant.objects.create(
            name="مستشفى الاختبار", subdomain="test", is_active=True
        )
        self.hospital = Hospital.objects.create(
            tenant=self.tenant,
            name="مستشفى الاختبار",
            address="دمشق، سوريا",
            phone="0911234567",
        )
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", email="test@example.com"
        )
        self.tenant_user = TenantUser.objects.create(
            user=self.user, tenant=self.tenant, role="admin"
        )
        self.client.force_authenticate(user=self.user)
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
            "tenant": self.tenant.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Hospital.objects.count(), 2)

    def test_update_hospital(self):
        """اختبار تحديث بيانات مستشفى"""
        url = reverse("hospital-detail", args=[self.hospital.id])
        data = {
            "name": "مستشفى الاختبار المحدث",
            "address": "دمشق، سوريا",
            "phone": "0911234567",
            "tenant": self.tenant.id,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.hospital.refresh_from_db()
        self.assertEqual(self.hospital.name, "مستشفى الاختبار المحدث")


class AuthenticationTest(APITestCase):
    def setUp(self):
        """إعداد بيانات الاختبار"""
        self.client = APIClient()
        self.tenant = Tenant.objects.create(
            name="مستشفى الاختبار", subdomain="test", is_active=True
        )
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", email="test@example.com"
        )
        self.tenant_user = TenantUser.objects.create(
            user=self.user, tenant=self.tenant, role="admin"
        )

    def test_login_required(self):
        """اختبار إلزامية تسجيل الدخول"""
        url = reverse("hospital-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_success(self):
        """اختبار نجاح تسجيل الدخول"""
        self.client.force_authenticate(user=self.user)
        url = reverse("hospital-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
