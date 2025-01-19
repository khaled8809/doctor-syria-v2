from datetime import timedelta

from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    Notification,
    NotificationPreference,
    NotificationTemplate,
    NotificationChannel,
    DeviceToken
)
from .serializers import (
    NotificationSerializer,
    NotificationPreferenceSerializer,
    NotificationTemplateSerializer,
    NotificationChannelSerializer,
    DeviceTokenSerializer
)
from .utils import send_push_notification, send_email_notification, send_sms_notification


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet للإشعارات مع وظائف متقدمة للإرسال والتتبع"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["is_read", "notification_type", "priority"]
    search_fields = ["title", "message", "notification_type"]
    ordering_fields = ["created_at", "priority", "is_read"]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """تحديد الإشعار كمقروء"""
        notification = self.get_object()
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        return Response({'status': 'تم تحديد الإشعار كمقروء'})

    @action(detail=True, methods=['post'])
    def mark_unread(self, request, pk=None):
        """تحديد الإشعار كغير مقروء"""
        notification = self.get_object()
        notification.is_read = False
        notification.read_at = None
        notification.save()
        return Response({'status': 'تم تحديد الإشعار كغير مقروء'})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """تحديد جميع الإشعارات كمقروءة"""
        self.get_queryset().filter(is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )
        return Response({'status': 'تم تحديد جميع الإشعارات كمقروءة'})

    @action(detail=False)
    def unread_count(self, request):
        """عدد الإشعارات غير المقروءة"""
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': count})

    @action(detail=False)
    def statistics(self, request):
        """إحصائيات الإشعارات"""
        queryset = self.get_queryset()
        total = queryset.count()
        unread = queryset.filter(is_read=False).count()
        by_type = queryset.values('notification_type').annotate(count=Count('id'))
        by_priority = queryset.values('priority').annotate(count=Count('id'))
        
        return Response({
            'total_notifications': total,
            'unread_notifications': unread,
            'by_type': by_type,
            'by_priority': by_priority
        })


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    """ViewSet لتفضيلات الإشعارات"""
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["notification_type", "channel", "is_enabled"]
    search_fields = ["notification_type", "channel"]
    ordering_fields = ["notification_type", "updated_at"]

    def get_queryset(self):
        return NotificationPreference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        """تحديث مجموعة من التفضيلات"""
        preferences = request.data.get('preferences', [])
        updated = []
        
        for pref in preferences:
            notification_type = pref.get('notification_type')
            channel = pref.get('channel')
            is_enabled = pref.get('is_enabled')
            
            if all([notification_type, channel, is_enabled is not None]):
                obj, created = NotificationPreference.objects.update_or_create(
                    user=request.user,
                    notification_type=notification_type,
                    channel=channel,
                    defaults={'is_enabled': is_enabled}
                )
                updated.append(self.get_serializer(obj).data)
        
        return Response({'updated_preferences': updated})


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet لقوالب الإشعارات"""
    serializer_class = NotificationTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["name", "notification_type", "template_content"]
    ordering_fields = ["name", "created_at"]

    def get_queryset(self):
        if self.request.user.is_staff:
            return NotificationTemplate.objects.all()
        return NotificationTemplate.objects.filter(is_active=True)

    @action(detail=True)
    def preview(self, request, pk=None):
        """معاينة قالب الإشعار"""
        template = self.get_object()
        test_data = request.query_params.dict()
        preview = template.render(test_data)
        return Response({'preview': preview})


class NotificationChannelViewSet(viewsets.ModelViewSet):
    """ViewSet لقنوات الإشعارات"""
    serializer_class = NotificationChannelSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]

    def get_queryset(self):
        if self.request.user.is_staff:
            return NotificationChannel.objects.all()
        return NotificationChannel.objects.filter(is_active=True)

    @action(detail=True)
    def test_channel(self, request, pk=None):
        """اختبار قناة الإشعارات"""
        channel = self.get_object()
        test_message = {
            'title': 'رسالة اختبار',
            'message': 'هذه رسالة اختبار للتأكد من عمل قناة الإشعارات',
            'data': {'test': True}
        }
        
        success = False
        if channel.channel_type == 'push':
            success = send_push_notification(request.user, test_message)
        elif channel.channel_type == 'email':
            success = send_email_notification(request.user.email, test_message)
        elif channel.channel_type == 'sms':
            success = send_sms_notification(request.user.phone_number, test_message)
        
        return Response({
            'success': success,
            'message': 'تم إرسال رسالة الاختبار بنجاح' if success else 'فشل إرسال رسالة الاختبار'
        })


class DeviceTokenViewSet(viewsets.ModelViewSet):
    """ViewSet لرموز الأجهزة"""
    serializer_class = DeviceTokenSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["device_type", "is_active"]
    search_fields = ["device_token", "device_name"]
    ordering_fields = ["created_at", "last_used_at"]

    def get_queryset(self):
        return DeviceToken.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # تحديث الرمز القديم للجهاز نفسه إن وجد
        device_token = serializer.validated_data.get('device_token')
        device_type = serializer.validated_data.get('device_type')
        
        DeviceToken.objects.filter(
            user=self.request.user,
            device_type=device_type,
            device_token=device_token
        ).update(is_active=False)
        
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """إلغاء تفعيل رمز الجهاز"""
        device_token = self.get_object()
        device_token.is_active = False
        device_token.save()
        return Response({'status': 'تم إلغاء تفعيل رمز الجهاز'})

    @action(detail=False)
    def active_devices(self, request):
        """الأجهزة النشطة"""
        devices = self.get_queryset().filter(is_active=True)
        return Response(self.get_serializer(devices, many=True).data)
