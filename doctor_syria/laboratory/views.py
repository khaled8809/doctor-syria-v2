from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import (
    TestCategory,
    LabTest,
    TestRequest,
    TestResult,
    SampleCollection,
    ReferenceRange,
)
from .serializers import (
    TestCategorySerializer,
    LabTestSerializer,
    TestRequestSerializer,
    TestResultSerializer,
    SampleCollectionSerializer,
    ReferenceRangeSerializer,
)


class LabTestListCreateView(generics.ListCreateAPIView):
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ["category"]
    search_fields = ["name", "category__name"]
    ordering_fields = ["name", "price"]


class LabTestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TestRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = TestRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["status", "laboratory"]
    search_fields = ["patient__user__first_name", "doctor__user__first_name"]
    ordering_fields = ["requested_date", "appointment_date"]

    def get_queryset(self):
        user = self.request.user
        if user.role == "laboratory":
            return TestRequest.objects.filter(laboratory__user=user)
        elif user.role == "doctor":
            return TestRequest.objects.filter(doctor__user=user)
        elif user.role == "patient":
            return TestRequest.objects.filter(patient__user=user)
        return TestRequest.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == "patient":
            serializer.save(patient=user.patient)
        elif user.role == "doctor":
            serializer.save(doctor=user.doctor)


class TestRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TestRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "laboratory":
            return TestRequest.objects.filter(laboratory__user=user)
        elif user.role == "doctor":
            return TestRequest.objects.filter(doctor__user=user)
        elif user.role == "patient":
            return TestRequest.objects.filter(patient__user=user)
        return TestRequest.objects.none()


class TestResultListCreateView(generics.ListCreateAPIView):
    serializer_class = TestResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["is_normal", "result_date"]
    search_fields = ["test_request__patient__user__first_name"]
    ordering_fields = ["result_date"]

    def get_queryset(self):
        user = self.request.user
        if user.role == "laboratory":
            return TestResult.objects.filter(test_request__laboratory__user=user)
        elif user.role == "doctor":
            return TestResult.objects.filter(test_request__doctor__user=user)
        elif user.role == "patient":
            return TestResult.objects.filter(test_request__patient__user=user)
        return TestResult.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role == "laboratory":
            serializer.save()


class TestResultDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TestResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "laboratory":
            return TestResult.objects.filter(test_request__laboratory__user=user)
        elif user.role == "doctor":
            return TestResult.objects.filter(test_request__doctor__user=user)
        elif user.role == "patient":
            return TestResult.objects.filter(test_request__patient__user=user)
        return TestResult.objects.none()


class SampleCollectionListCreateView(generics.ListCreateAPIView):
    serializer_class = SampleCollectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["status", "collection_date"]
    search_fields = ["test_request__patient__user__first_name"]
    ordering_fields = ["collection_date"]

    def get_queryset(self):
        user = self.request.user
        if user.role == "laboratory":
            return SampleCollection.objects.filter(test_request__laboratory__user=user)
        return SampleCollection.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role == "laboratory":
            serializer.save()


class SampleCollectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SampleCollectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "laboratory":
            return SampleCollection.objects.filter(test_request__laboratory__user=user)
        return SampleCollection.objects.none()
