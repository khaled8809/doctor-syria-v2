from django.contrib.auth import get_user_model
from django.db import connection, reset_queries
from django.test import Client, TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone

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
    Warehouse,
)

User = get_user_model()


class DatabaseOptimizationTest(TestCase):
    def setUp(self):
        """إعداد بيانات الاختبار"""
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
        # إنشاء 10 أطباء
        self.doctors = []
        for i in range(10):
            user = User.objects.create_user(
                username=f"doctor{i}",
                password="testpass123",
                first_name=f"طبيب{i}",
                last_name="اختبار",
            )
            doctor = Doctor.objects.create(
                tenant=self.tenant,
                user=user,
                specialization="تخصص عام",
                license_number=f"LIC{i}001",
                phone=f"09{i}1234567",
            )
            self.doctors.append(doctor)

        # إنشاء 5 أقسام
        self.departments = []
        for i in range(5):
            department = Department.objects.create(
                hospital=self.hospital,
                name=f"قسم {i}",
                specialty=f"تخصص {i}",
                head_doctor=self.doctors[i],
                capacity=20,
                available_beds=10,
                floor=str(i + 1),
                phone_extension=f"1{i}01",
            )
            self.departments.append(department)

        # إنشاء 20 مريض
        self.patients = []
        for i in range(20):
            patient = Patient.objects.create(
                tenant=self.tenant,
                name=f"مريض{i} اختبار",
                age=30 + i,
                gender="ذكر" if i % 2 == 0 else "أنثى",
                condition="حالة مستقرة",
            )
            self.patients.append(patient)

        # إنشاء مستودع ومستلزمات طبية
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
            manager=self.doctors[0].user,
        )

        # إنشاء 10 مستلزمات طبية
        self.supplies = []
        for i in range(10):
            supply = MedicalSupply.objects.create(
                tenant=self.tenant,
                name=f"مستلزم{i}",
                code=f"SUP{i}001",
                supply_type="DISPOSABLE",
                manufacturer=self.company,
                description=f"وصف المستلزم {i}",
                unit="قطعة",
                minimum_quantity=10,
                storage_condition="NORMAL",
            )
            self.supplies.append(supply)

    def test_hospital_departments_query_count(self):
        """اختبار عدد الاستعلامات عند جلب الأقسام"""
        with CaptureQueriesContext(connection) as context:
            # استعلام غير محسن
            departments = Department.objects.filter(hospital=self.hospital)
            for dept in departments:
                _ = dept.head_doctor.user.username

            unoptimized_query_count = len(context.captured_queries)

        with CaptureQueriesContext(connection) as context:
            # استعلام محسن باستخدام select_related
            departments = Department.objects.select_related(
                "head_doctor", "head_doctor__user"
            ).filter(hospital=self.hospital)
            for dept in departments:
                _ = dept.head_doctor.user.username

            optimized_query_count = len(context.captured_queries)

        self.assertLess(
            optimized_query_count,
            unoptimized_query_count,
            "الاستعلام المحسن يجب أن يستخدم عدد أقل من الاستعلامات",
        )

    def test_patient_admissions_query_count(self):
        """اختبار عدد الاستعلامات عند جلب سجلات الدخول"""
        # إنشاء سجلات دخول للمرضى
        for i in range(5):
            Admission.objects.create(
                patient=self.patients[i],
                hospital=self.hospital,
                department=self.departments[0],
                doctor=self.doctors[0],
                admission_date=timezone.now(),
                reason="فحص دوري",
                diagnosis="حالة مستقرة",
                treatment_plan="متابعة",
                room_number=f"R{i}01",
                bed_number=f"B{i}01",
                status="ADMITTED",
            )

        with CaptureQueriesContext(connection) as context:
            # استعلام غير محسن
            admissions = Admission.objects.filter(hospital=self.hospital)
            for admission in admissions:
                _ = admission.patient.name
                _ = admission.doctor.specialization
                _ = admission.department.name

            unoptimized_query_count = len(context.captured_queries)

        with CaptureQueriesContext(connection) as context:
            # استعلام محسن باستخدام select_related
            admissions = Admission.objects.select_related(
                "patient", "doctor", "department"
            ).filter(hospital=self.hospital)
            for admission in admissions:
                _ = admission.patient.name
                _ = admission.doctor.specialization
                _ = admission.department.name

            optimized_query_count = len(context.captured_queries)

        self.assertLess(
            optimized_query_count,
            unoptimized_query_count,
            "الاستعلام المحسن يجب أن يستخدم عدد أقل من الاستعلامات",
        )

    def test_inventory_items_query_count(self):
        """اختبار عدد الاستعلامات عند جلب عناصر المخزون"""
        # إنشاء عناصر مخزون
        for i in range(5):
            InventoryItem.objects.create(
                tenant=self.tenant,
                supply=self.supplies[i],
                warehouse=self.warehouse,
                batch_number=f"BATCH{i}001",
                quantity=100,
                unit_price=10.0,
                manufacturing_date=timezone.now().date(),
                expiry_date=timezone.now().date() + timezone.timedelta(days=365),
                location_in_warehouse=f"A{i}-B{i}-C{i}",
            )

        with CaptureQueriesContext(connection) as context:
            # استعلام غير محسن
            items = InventoryItem.objects.filter(warehouse=self.warehouse)
            for item in items:
                _ = item.supply.name
                _ = item.warehouse.name

            unoptimized_query_count = len(context.captured_queries)

        with CaptureQueriesContext(connection) as context:
            # استعلام محسن باستخدام select_related
            items = InventoryItem.objects.select_related("supply", "warehouse").filter(
                warehouse=self.warehouse
            )
            for item in items:
                _ = item.supply.name
                _ = item.warehouse.name

            optimized_query_count = len(context.captured_queries)

        self.assertLess(
            optimized_query_count,
            unoptimized_query_count,
            "الاستعلام المحسن يجب أن يستخدم عدد أقل من الاستعلامات",
        )
