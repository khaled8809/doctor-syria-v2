from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Doctor, Patient, Pharmacy, Laboratory, PharmaceuticalCompany

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 
                 'phone_number', 'address', 'profile_image')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Doctor
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'doctor'
        user = User.objects.create_user(**user_data)
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'patient'
        user = User.objects.create_user(**user_data)
        patient = Patient.objects.create(user=user, **validated_data)
        return patient

class PharmacySerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Pharmacy
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'pharmacy'
        user = User.objects.create_user(**user_data)
        pharmacy = Pharmacy.objects.create(user=user, **validated_data)
        return pharmacy

class LaboratorySerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Laboratory
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'laboratory'
        user = User.objects.create_user(**user_data)
        laboratory = Laboratory.objects.create(user=user, **validated_data)
        return laboratory

class PharmaceuticalCompanySerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = PharmaceuticalCompany
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'company'
        user = User.objects.create_user(**user_data)
        company = PharmaceuticalCompany.objects.create(user=user, **validated_data)
        return company
