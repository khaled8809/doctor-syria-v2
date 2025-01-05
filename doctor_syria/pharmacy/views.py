from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .models import (Medicine, PharmacyInventory, MedicineOrder, OrderItem,
                    DeliveryAddress, MedicineCategory, Pharmacy)
from .serializers import (MedicineSerializer, PharmacyInventorySerializer,
                         MedicineOrderSerializer, OrderItemSerializer,
                         DeliveryAddressSerializer, MedicineCategorySerializer)

class PharmacyListView(LoginRequiredMixin, ListView):
    model = Pharmacy
    template_name = 'pharmacy/pharmacy_list.html'
    context_object_name = 'pharmacies'
    paginate_by = 10

    def get_queryset(self):
        return Pharmacy.objects.all()

class PharmacyDetailView(LoginRequiredMixin, DetailView):
    model = Pharmacy
    template_name = 'pharmacy/pharmacy_detail.html'
    context_object_name = 'pharmacy'

class MedicineListCreateView(generics.ListCreateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ['requires_prescription', 'manufacturer']
    search_fields = ['name', 'scientific_name', 'manufacturer__name']
    ordering_fields = ['name', 'price']

class MedicineDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PharmacyInventoryListView(generics.ListCreateAPIView):
    serializer_class = PharmacyInventorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['medicine', 'quantity']
    search_fields = ['medicine__name', 'batch_number']
    ordering_fields = ['expiry_date', 'quantity']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'pharmacy':
            return PharmacyInventory.objects.filter(pharmacy__user=user)
        return PharmacyInventory.objects.none()

    def perform_create(self, serializer):
        serializer.save(pharmacy=self.request.user.pharmacy)

class PharmacyInventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PharmacyInventorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'pharmacy':
            return PharmacyInventory.objects.filter(pharmacy__user=user)
        return PharmacyInventory.objects.none()

class MedicineOrderListCreateView(generics.ListCreateAPIView):
    serializer_class = MedicineOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'order_date']
    search_fields = ['pharmacy__name']
    ordering_fields = ['order_date', 'total_amount']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'pharmacy':
            return MedicineOrder.objects.filter(pharmacy__user=user)
        elif user.role == 'company':
            return MedicineOrder.objects.filter(items__medicine__manufacturer__user=user)
        return MedicineOrder.objects.none()

    def perform_create(self, serializer):
        serializer.save(pharmacy=self.request.user.pharmacy)

class MedicineOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MedicineOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'pharmacy':
            return MedicineOrder.objects.filter(pharmacy__user=user)
        elif user.role == 'company':
            return MedicineOrder.objects.filter(items__medicine__manufacturer__user=user)
        return MedicineOrder.objects.none()

class MedicineCategoryListView(generics.ListCreateAPIView):
    queryset = MedicineCategory.objects.all()
    serializer_class = MedicineCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ['name']
    ordering_fields = ['name']

class MedicineCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MedicineCategory.objects.all()
    serializer_class = MedicineCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
