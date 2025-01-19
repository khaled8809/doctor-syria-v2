from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from saas_core.models import Tenant, TenantUser

from ..models import Doctor, Hospital

User = get_user_model()


class AuthenticationTest(APITestCase):
    def setUp(self):
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

    def test_login_success(self):
        """اختبار تسجيل الدخول الناجح"""
        url = reverse("token_obtain_pair")
        data = {"username": "testuser", "password": "testpass123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_failure(self):
        """اختبار تسجيل الدخول الفاشل"""
        url = reverse("token_obtain_pair")
        data = {"username": "testuser", "password": "wrongpass"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthorizationTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # إنشاء مستأجر
        self.tenant = Tenant.objects.create(
            name="مستشفى الاختبار", subdomain="test", is_active=True
        )

        # إنشاء مستخدم مدير
        self.admin_user = User.objects.create_user(
            username="admin", password="admin123", is_staff=True
        )
        self.admin_tenant_user = TenantUser.objects.create(
            user=self.admin_user, tenant=self.tenant, role="admin"
        )

        # إنشاء مستخدم طبيب
        self.doctor_user = User.objects.create_user(
            username="doctor", password="doctor123"
        )
        self.doctor_tenant_user = TenantUser.objects.create(
            user=self.doctor_user, tenant=self.tenant, role="doctor"
        )

        # إنشاء مستخدم موظف
        self.staff_user = User.objects.create_user(
            username="staff", password="staff123"
        )
        self.staff_tenant_user = TenantUser.objects.create(
            user=self.staff_user, tenant=self.tenant, role="staff"
        )

        # إنشاء مستشفى للاختبار
        self.hospital = Hospital.objects.create(
            tenant=self.tenant, name="مستشفى الاختبار"
        )

    def test_admin_access(self):
        """اختبار صلاحيات المدير"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("hospital-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # اختبار إنشاء مستشفى جديد
        data = {"name": "مستشفى جديد", "tenant": self.tenant.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_doctor_access(self):
        """اختبار صلاحيات الطبيب"""
        self.client.force_authenticate(user=self.doctor_user)

        # اختبار الوصول إلى قائمة المستشفيات (مسموح)
        url = reverse("hospital-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # اختبار إنشاء مستشفى جديد (غير مسموح)
        data = {"name": "مستشفى جديد", "tenant": self.tenant.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_access(self):
        """اختبار صلاحيات الموظف"""
        self.client.force_authenticate(user=self.staff_user)

        # اختبار الوصول إلى قائمة المستشفيات (مسموح)
        url = reverse("hospital-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # اختبار إنشاء مستشفى جديد (غير مسموح)
        data = {"name": "مستشفى جديد", "tenant": self.tenant.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_access(self):
        """اختبار الوصول بدون تسجيل دخول"""
        url = reverse("hospital-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
