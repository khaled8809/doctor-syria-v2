from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from core.serializers import BaseModelSerializer

from .validators import validate_password_strength

User = get_user_model()


class UserSerializer(BaseModelSerializer):
    """
    المسلسل الأساسي للمستخدم
    """

    full_name = serializers.CharField(source="get_full_name", read_only=True)
    password = serializers.CharField(
        write_only=True, required=False, validators=[validate_password_strength]
    )

    class Meta:
        model = User
        fields = BaseModelSerializer.Meta.fields + [
            "email",
            "phone",
            "user_type",
            "full_name",
            "first_name",
            "last_name",
            "father_name",
            "mother_name",
            "birth_date",
            "gender",
            "marital_status",
            "blood_type",
            "id_type",
            "id_number",
            "address",
            "city",
            "region",
            "is_verified",
            "password",
        ]
        read_only_fields = ["is_verified", "verification_date", "last_login_ip"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class DoctorSerializer(UserSerializer):
    """
    مسلسل خاص بالأطباء
    """

    rating = serializers.FloatField(read_only=True)
    reviews_count = serializers.IntegerField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + [
            "specialty",
            "license_number",
            "qualification",
            "experience_years",
            "rating",
            "reviews_count",
            "license_picture",
        ]

    def validate(self, data):
        if data.get("user_type") != "doctor":
            raise serializers.ValidationError(_("نوع المستخدم يجب أن يكون طبيب"))
        return data


class PatientSerializer(UserSerializer):
    """
    مسلسل خاص بالمرضى
    """

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ["blood_type", "emergency_contact"]

    def validate(self, data):
        if data.get("user_type") != "patient":
            raise serializers.ValidationError(_("نوع المستخدم يجب أن يكون مريض"))
        return data


class PharmacySerializer(UserSerializer):
    """
    مسلسل خاص بالصيدليات
    """

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + [
            "license_number",
            "license_picture",
            "working_hours",
            "delivery_available",
        ]

    def validate(self, data):
        if data.get("user_type") != "pharmacy":
            raise serializers.ValidationError(_("نوع المستخدم يجب أن يكون صيدلية"))
        return data


class LaboratorySerializer(UserSerializer):
    """
    مسلسل خاص بالمختبرات
    """

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + [
            "license_number",
            "license_picture",
            "working_hours",
            "home_service_available",
        ]

    def validate(self, data):
        if data.get("user_type") != "lab":
            raise serializers.ValidationError(_("نوع المستخدم يجب أن يكون مختبر"))
        return data


class PharmaceuticalCompanySerializer(UserSerializer):
    """
    مسلسل خاص بشركات الأدوية
    """

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + [
            "license_number",
            "license_picture",
            "company_name",
            "registration_number",
        ]

    def validate(self, data):
        if data.get("user_type") != "company":
            raise serializers.ValidationError(_("نوع المستخدم يجب أن يكون شركة أدوية"))
        return data


class UserProfilePictureSerializer(serializers.ModelSerializer):
    """
    مسلسل خاص بتحديث الصورة الشخصية
    """

    class Meta:
        model = User
        fields = ["profile_picture"]


class ChangePasswordSerializer(serializers.Serializer):
    """
    مسلسل خاص بتغيير كلمة المرور
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True, validators=[validate_password_strength]
    )

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(_("كلمة المرور الحالية غير صحيحة"))
        return value


"""
Serializers for the accounts application.
"""
from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    class Meta:
        model = models.User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'date_of_birth', 'gender']
        read_only_fields = ['id']


class SpecializationSerializer(serializers.ModelSerializer):
    """
    Serializer for Specialization model.
    """
    class Meta:
        model = models.Specialization
        fields = ['id', 'name', 'name_ar', 'description', 'description_ar']
        read_only_fields = ['id']


class DoctorSerializer(serializers.ModelSerializer):
    """
    Serializer for Doctor model.
    """
    user = UserSerializer()
    specialization = SpecializationSerializer()

    class Meta:
        model = models.Doctor
        fields = ['id', 'user', 'specialization', 'license_number', 'years_of_experience', 'bio', 'bio_ar', 'rating']
        read_only_fields = ['id', 'rating']


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient model.
    """
    user = UserSerializer()

    class Meta:
        model = models.Patient
        fields = ['id', 'user', 'blood_type', 'emergency_contact', 'emergency_phone']
        read_only_fields = ['id']


class InsuranceSerializer(serializers.ModelSerializer):
    """
    Serializer for Insurance model.
    """
    patient = PatientSerializer()

    class Meta:
        model = models.Insurance
        fields = ['id', 'patient', 'provider', 'policy_number', 'expiry_date', 'coverage_details']
        read_only_fields = ['id']
