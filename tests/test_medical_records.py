import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from medical_records.models import MedicalRecord, Prescription, VitalSigns

from accounts.models import User


@pytest.mark.django_db
class TestMedicalRecord:
    """اختبارات السجلات الطبية"""

    @pytest.fixture
    def patient(self):
        return User.objects.create(
            username="patient", email="patient@test.com", role="patient"
        )

    @pytest.fixture
    def doctor(self):
        return User.objects.create(
            username="doctor", email="doctor@test.com", role="doctor"
        )

    @pytest.fixture
    def medical_record(self, patient, doctor):
        return MedicalRecord.objects.create(
            patient=patient,
            doctor=doctor,
            diagnosis="Test Diagnosis",
            treatment_plan="Test Treatment",
        )

    def test_create_medical_record(self, patient, doctor):
        """اختبار إنشاء سجل طبي"""
        record = MedicalRecord.objects.create(
            patient=patient, doctor=doctor, diagnosis="Test", treatment_plan="Test Plan"
        )
        assert record.pk is not None
        assert record.patient == patient
        assert record.doctor == doctor

    def test_add_vital_signs(self, medical_record, doctor):
        """اختبار إضافة العلامات الحيوية"""
        vital_signs = VitalSigns.objects.create(
            medical_record=medical_record,
            temperature=37.5,
            blood_pressure_systolic=120,
            blood_pressure_diastolic=80,
            heart_rate=75,
            respiratory_rate=16,
            oxygen_saturation=98,
            recorded_by=doctor,
        )
        assert vital_signs.pk is not None
        assert vital_signs.temperature == 37.5

    def test_add_prescription(self, medical_record, doctor):
        """اختبار إضافة وصفة طبية"""
        prescription = Prescription.objects.create(
            medical_record=medical_record,
            medicine_name="Test Medicine",
            dosage="1 pill",
            frequency="twice daily",
            duration="7 days",
            prescribed_by=doctor,
        )
        assert prescription.pk is not None
        assert prescription.medicine_name == "Test Medicine"

    def test_invalid_vital_signs(self, medical_record, doctor):
        """اختبار القيم غير الصالحة للعلامات الحيوية"""
        with pytest.raises(ValidationError):
            VitalSigns.objects.create(
                medical_record=medical_record,
                temperature=45,  # درجة حرارة غير واقعية
                blood_pressure_systolic=120,
                blood_pressure_diastolic=80,
                heart_rate=75,
                respiratory_rate=16,
                oxygen_saturation=98,
                recorded_by=doctor,
            )

    def test_medical_record_history(self, medical_record, doctor):
        """اختبار تاريخ السجل الطبي"""
        # إضافة علامات حيوية متعددة
        for _ in range(3):
            VitalSigns.objects.create(
                medical_record=medical_record,
                temperature=37.5,
                blood_pressure_systolic=120,
                blood_pressure_diastolic=80,
                heart_rate=75,
                respiratory_rate=16,
                oxygen_saturation=98,
                recorded_by=doctor,
            )

        assert medical_record.vital_signs.count() == 3

    def test_prescription_fill(self, medical_record, doctor):
        """اختبار صرف الوصفة الطبية"""
        prescription = Prescription.objects.create(
            medical_record=medical_record,
            medicine_name="Test Medicine",
            dosage="1 pill",
            frequency="twice daily",
            duration="7 days",
            prescribed_by=doctor,
        )

        # صرف الوصفة
        prescription.filled = True
        prescription.filled_by = doctor
        prescription.filled_at = timezone.now()
        prescription.save()

        assert prescription.filled is True
        assert prescription.filled_by == doctor
        assert prescription.filled_at is not None

    def test_medical_record_permissions(self, medical_record, patient):
        """اختبار صلاحيات السجل الطبي"""
        unauthorized_user = User.objects.create(
            username="unauthorized", email="unauthorized@test.com", role="patient"
        )

        # المريض يمكنه الوصول إلى سجله
        assert patient.medical_records.filter(pk=medical_record.pk).exists()

        # مستخدم آخر لا يمكنه الوصول
        assert not unauthorized_user.medical_records.filter(
            pk=medical_record.pk
        ).exists()
