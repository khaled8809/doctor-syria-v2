from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import Allergy, Appointment, MedicalRecord, Prescription, Vaccination


class MedicalRecordSerializer(serializers.ModelSerializer):
    """
    مسلسل السجل الطبي
    """

    patient = UserSerializer(read_only=True)
    doctor = UserSerializer(read_only=True)
    record_type_display = serializers.CharField(
        source="get_record_type_display", read_only=True
    )
    severity_display = serializers.CharField(
        source="get_severity_display", read_only=True
    )

    class Meta:
        model = MedicalRecord
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "created_by", "updated_by")


class AppointmentSerializer(serializers.ModelSerializer):
    """
    مسلسل المواعيد
    """

    patient = UserSerializer(read_only=True)
    doctor = UserSerializer(read_only=True)
    appointment_type_display = serializers.CharField(
        source="get_appointment_type_display", read_only=True
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "created_by", "updated_by")

    def validate_scheduled_time(self, value):
        """
        التحقق من وقت الموعد
        """
        if value < timezone.now():
            raise serializers.ValidationError("لا يمكن تحديد موعد في الماضي")
        return value

    def validate(self, data):
        """
        التحقق من تعارض المواعيد
        """
        doctor = data.get("doctor")
        scheduled_time = data.get("scheduled_time")
        duration = data.get("duration", 30)

        if doctor and scheduled_time:
            # التحقق من وجود مواعيد متعارضة
            conflicting_appointments = Appointment.objects.filter(
                doctor=doctor,
                scheduled_time__range=(
                    scheduled_time,
                    scheduled_time + timezone.timedelta(minutes=duration),
                ),
                status=AppointmentStatus.CONFIRMED,
            ).exclude(pk=self.instance.pk if self.instance else None)

            if conflicting_appointments.exists():
                raise serializers.ValidationError(
                    "يوجد موعد آخر في نفس الوقت مع نفس الطبيب"
                )

        return data


class PrescriptionSerializer(serializers.ModelSerializer):
    """
    مسلسل الوصفات الطبية
    """

    medical_record = MedicalRecordSerializer(read_only=True)

    class Meta:
        model = Prescription
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "created_by", "updated_by")


class AllergySerializer(serializers.ModelSerializer):
    """
    مسلسل الحساسية
    """

    patient = UserSerializer(read_only=True)
    allergy_type_display = serializers.CharField(
        source="get_allergy_type_display", read_only=True
    )
    reaction_display = serializers.CharField(
        source="get_reaction_display", read_only=True
    )

    class Meta:
        model = Allergy
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "created_by", "updated_by")


class VaccinationSerializer(serializers.ModelSerializer):
    """
    مسلسل التطعيمات
    """

    patient = UserSerializer(read_only=True)
    given_by = UserSerializer(read_only=True)
    vaccine_type_display = serializers.CharField(
        source="get_vaccine_type_display", read_only=True
    )

    class Meta:
        model = Vaccination
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "created_by", "updated_by")

    def validate(self, data):
        """
        التحقق من تسلسل جرعات التطعيم
        """
        patient = data.get("patient")
        vaccine_type = data.get("vaccine_type")
        dose_number = data.get("dose_number", 1)

        if patient and vaccine_type and dose_number > 1:
            # التحقق من وجود الجرعات السابقة
            previous_doses = Vaccination.objects.filter(
                patient=patient, vaccine_type=vaccine_type, dose_number__lt=dose_number
            ).count()

            if previous_doses != dose_number - 1:
                raise serializers.ValidationError(
                    "يجب إدخال الجرعات السابقة قبل إضافة هذه الجرعة"
                )

        return data
