from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Appointment, Schedule


class AppointmentSerializer(serializers.ModelSerializer):
    """
    مسلسل المواعيد
    Appointment serializer with validation and additional fields
    """

    doctor_name = serializers.CharField(source="doctor.get_full_name", read_only=True)
    patient_name = serializers.CharField(source="patient.get_full_name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    priority_display = serializers.CharField(
        source="get_priority_display", read_only=True
    )

    class Meta:
        model = Appointment
        fields = [
            "id",
            "patient",
            "doctor",
            "doctor_name",
            "patient_name",
            "appointment_date",
            "reason",
            "status",
            "status_display",
            "priority",
            "priority_display",
            "notes",
            "created_at",
            "updated_at",
            "reminder_sent",
        ]
        read_only_fields = ["created_at", "updated_at", "reminder_sent"]

    def validate_appointment_date(self, value):
        """
        التحقق من صحة تاريخ الموعد
        Validate appointment date
        """
        if value < timezone.now():
            raise serializers.ValidationError(
                _("Appointment date cannot be in the past")
            )

        # التحقق من توفر الطبيب | Check doctor availability
        doctor = self.initial_data.get("doctor")
        if doctor:
            schedule = Schedule.objects.filter(
                doctor_id=doctor, day_of_week=value.weekday(), is_available=True
            ).first()

            if not schedule:
                raise serializers.ValidationError(
                    _("Doctor is not available on this day")
                )

            # التحقق من وقت الموعد | Check appointment time
            appointment_time = value.time()
            if not (schedule.start_time <= appointment_time <= schedule.end_time):
                raise serializers.ValidationError(
                    _("Appointment time is outside doctor's working hours")
                )

            # التحقق من تداخل المواعيد | Check for appointment conflicts
            existing_appointments = Appointment.objects.filter(
                doctor_id=doctor,
                appointment_date__date=value.date(),
                status="confirmed",
            )

            for existing_appointment in existing_appointments:
                if (
                    abs((existing_appointment.appointment_date - value).total_seconds())
                    < schedule.appointment_duration * 60
                ):
                    raise serializers.ValidationError(
                        _("This time slot is already booked")
                    )

        return value

    def validate(self, data):
        """
        التحقق من صحة البيانات
        Validate the data
        """
        if self.instance and self.instance.status == "cancelled":
            raise serializers.ValidationError(
                _("Cannot modify a cancelled appointment")
            )

        return data

    def create(self, validated_data):
        """
        إنشاء موعد جديد
        Create a new appointment
        """
        validated_data["status"] = "pending"
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        تحديث موعد
        Update an appointment
        """
        if instance.status == "cancelled":
            raise serializers.ValidationError(
                _("Cannot modify a cancelled appointment")
            )

        return super().update(instance, validated_data)
