from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Report, MedicalDevice, DeviceReading, AIModel, AIPrediction,
    Resource, ResourceSchedule, ChatRoom, Message, VideoCall
)
from .serializers import (
    ReportSerializer, MedicalDeviceSerializer, DeviceReadingSerializer,
    AIModelSerializer, AIPredictionSerializer, ResourceSerializer,
    ResourceScheduleSerializer, ChatRoomSerializer, MessageSerializer,
    VideoCallSerializer
)

class TenantModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        return self.queryset.filter(tenant=self.request.tenant)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant)

class ReportViewSet(TenantModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filterset_fields = ['report_type', 'created_at']
    search_fields = ['title']
    ordering_fields = ['created_at']

    @action(detail=True, methods=['post'])
    def generate_pdf(self, request, pk=None):
        report = self.get_object()
        # Здесь будет логика генерации PDF
        return Response({'status': 'PDF generation started'})

class MedicalDeviceViewSet(TenantModelViewSet):
    queryset = MedicalDevice.objects.all()
    serializer_class = MedicalDeviceSerializer
    filterset_fields = ['device_type', 'is_active']
    search_fields = ['name', 'model_number', 'serial_number']
    ordering_fields = ['name', 'last_maintenance']

    @action(detail=True, methods=['post'])
    def schedule_maintenance(self, request, pk=None):
        device = self.get_object()
        # Логика планирования обслуживания
        return Response({'status': 'Maintenance scheduled'})

class DeviceReadingViewSet(TenantModelViewSet):
    queryset = DeviceReading.objects.all()
    serializer_class = DeviceReadingSerializer
    filterset_fields = ['device', 'reading_type', 'timestamp']
    ordering_fields = ['timestamp']

class AIModelViewSet(TenantModelViewSet):
    queryset = AIModel.objects.all()
    serializer_class = AIModelSerializer
    filterset_fields = ['model_type', 'is_active']
    search_fields = ['name']
    ordering_fields = ['accuracy', 'last_trained']

    @action(detail=True, methods=['post'])
    def train_model(self, request, pk=None):
        model = self.get_object()
        # Логика обучения модели
        return Response({'status': 'Training started'})

class AIPredictionViewSet(TenantModelViewSet):
    queryset = AIPrediction.objects.all()
    serializer_class = AIPredictionSerializer
    filterset_fields = ['model', 'prediction_type', 'is_accurate']
    ordering_fields = ['confidence_score', 'timestamp']

class ResourceViewSet(TenantModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    filterset_fields = ['resource_type', 'status']
    search_fields = ['name']
    ordering_fields = ['current_usage']

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        resource = self.get_object()
        schedule = resource.resourceschedule_set.filter(status='SCHEDULED')
        return Response({
            'current_usage': resource.current_usage,
            'capacity': resource.capacity,
            'scheduled_events': ResourceScheduleSerializer(schedule, many=True).data
        })

class ResourceScheduleViewSet(TenantModelViewSet):
    queryset = ResourceSchedule.objects.all()
    serializer_class = ResourceScheduleSerializer
    filterset_fields = ['resource', 'status', 'assigned_to']
    ordering_fields = ['start_time']

class ChatRoomViewSet(TenantModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    filterset_fields = ['is_group']
    search_fields = ['name']
    ordering_fields = ['last_activity']

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        chat_room = self.get_object()
        messages = chat_room.message_set.all().order_by('-created_at')
        page = self.paginate_queryset(messages)
        serializer = MessageSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

class MessageViewSet(TenantModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filterset_fields = ['chat_room', 'message_type', 'is_read']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class VideoCallViewSet(TenantModelViewSet):
    queryset = VideoCall.objects.all()
    serializer_class = VideoCallSerializer
    filterset_fields = ['status', 'chat_room']
    ordering_fields = ['start_time']

    @action(detail=True, methods=['post'])
    def end_call(self, request, pk=None):
        call = self.get_object()
        # Логика завершения звонка
        return Response({'status': 'Call ended'})
