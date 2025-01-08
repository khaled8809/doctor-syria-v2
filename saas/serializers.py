from rest_framework import serializers
from .models import (
    Report, MedicalDevice, DeviceReading, AIModel, AIPrediction,
    Resource, ResourceSchedule, ChatRoom, Message, VideoCall
)

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ('tenant', 'created_by', 'created_at')

class MedicalDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalDevice
        fields = '__all__'
        read_only_fields = ('tenant',)

class DeviceReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceReading
        fields = '__all__'

class AIModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIModel
        fields = '__all__'
        read_only_fields = ('tenant', 'accuracy', 'last_trained')

class AIPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIPrediction
        fields = '__all__'
        read_only_fields = ('timestamp', 'verified_by')

class ResourceSerializer(serializers.ModelSerializer):
    availability_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = '__all__'
        read_only_fields = ('tenant', 'current_usage')

    def get_availability_percentage(self, obj):
        if obj.capacity == 0:
            return 0
        return ((obj.capacity - obj.current_usage) / obj.capacity) * 100

class ResourceScheduleSerializer(serializers.ModelSerializer):
    resource_name = serializers.CharField(source='resource.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)

    class Meta:
        model = ResourceSchedule
        fields = '__all__'
        read_only_fields = ('status',)

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must be after start time")
        return data

class ChatRoomSerializer(serializers.ModelSerializer):
    participant_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = '__all__'
        read_only_fields = ('tenant', 'created_at', 'last_activity')

    def get_participant_count(self, obj):
        return obj.participants.count()

    def get_last_message(self, obj):
        last_msg = obj.message_set.order_by('-created_at').first()
        if last_msg:
            return {
                'content': last_msg.content[:50],
                'sender': last_msg.sender.get_full_name(),
                'timestamp': last_msg.created_at
            }
        return None

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('sender', 'created_at', 'is_read')

class VideoCallSerializer(serializers.ModelSerializer):
    initiator_name = serializers.CharField(source='initiator.get_full_name', read_only=True)
    duration = serializers.SerializerMethodField()

    class Meta:
        model = VideoCall
        fields = '__all__'
        read_only_fields = ('initiator', 'start_time', 'end_time')

    def get_duration(self, obj):
        if obj.end_time and obj.start_time:
            return (obj.end_time - obj.start_time).total_seconds()
        return None
