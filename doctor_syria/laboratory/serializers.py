from rest_framework import serializers

from accounts.serializers import (
    DoctorSerializer,
    LaboratorySerializer,
    PatientSerializer,
)

from .models import (
    LabTest,
    ReferenceRange,
    SampleCollection,
    TestCategory,
    TestRequest,
    TestResult,
)


class TestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCategory
        fields = "__all__"


class ReferenceRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceRange
        fields = "__all__"


class LabTestSerializer(serializers.ModelSerializer):
    category = TestCategorySerializer(read_only=True)
    reference_ranges = ReferenceRangeSerializer(many=True, read_only=True)

    class Meta:
        model = LabTest
        fields = "__all__"


class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = "__all__"


class SampleCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleCollection
        fields = "__all__"


class TestRequestSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    laboratory = LaboratorySerializer(read_only=True)
    test = LabTestSerializer(read_only=True)
    result = TestResultSerializer(read_only=True)
    sample = SampleCollectionSerializer(read_only=True)

    class Meta:
        model = TestRequest
        fields = "__all__"

    def validate(self, data):
        # Add validation logic here (e.g., check if laboratory is available)
        return data
