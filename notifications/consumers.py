import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = f"notifications_{self.user.id}"

        # الانضمام إلى غرفة المستخدم
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # مغادرة غرفة المستخدم
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """استقبال الرسائل من العميل"""
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'mark_read':
            await self.mark_notifications_read(data.get('notification_ids', []))
        elif message_type == 'get_unread':
            await self.send_unread_notifications()

    async def notification(self, event):
        """إرسال إشعار للمستخدم"""
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': event['message'],
            'data': event['data']
        }))

    @database_sync_to_async
    def mark_notifications_read(self, notification_ids):
        """تحديث حالة الإشعارات إلى مقروءة"""
        from .models import Notification
        Notification.objects.filter(
            id__in=notification_ids,
            user=self.user
        ).update(
            read_at=timezone.now()
        )

    @database_sync_to_async
    def send_unread_notifications(self):
        """إرسال الإشعارات غير المقروءة"""
        from .models import Notification
        notifications = Notification.objects.filter(
            user=self.user,
            read_at__isnull=True
        ).values('id', 'message', 'created_at', 'data')
        
        return self.send(text_data=json.dumps({
            'type': 'unread_notifications',
            'notifications': list(notifications)
        }))
