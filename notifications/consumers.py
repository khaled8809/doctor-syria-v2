"""
مستهلك WebSocket للإشعارات
"""

import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone

from .models import Notification


class NotificationConsumer(AsyncWebsocketConsumer):
    """مستهلك WebSocket للإشعارات"""

    async def connect(self):
        """عند الاتصال"""
        if self.scope["user"].is_anonymous:
            await self.close()
            return

        self.user_id = self.scope["user"].id
        self.group_name = f"notifications_{self.user_id}"

        # الانضمام إلى مجموعة الإشعارات
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # إرسال الإشعارات غير المقروءة عند الاتصال
        unread_notifications = await self.get_unread_notifications()
        if unread_notifications:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "unread_notifications",
                        "notifications": unread_notifications,
                    }
                )
            )

    async def disconnect(self, close_code):
        """عند قطع الاتصال"""
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        """عند استلام رسالة"""
        try:
            data = json.loads(text_data)
            action = data.get("action")

            if action == "mark_as_read":
                notification_id = data.get("notification_id")
                if notification_id:
                    success = await self.mark_notification_as_read(notification_id)
                    await self.send(
                        text_data=json.dumps(
                            {
                                "type": "mark_as_read_response",
                                "notification_id": notification_id,
                                "success": success,
                            }
                        )
                    )

            elif action == "mark_all_as_read":
                await self.mark_all_notifications_as_read()
                await self.send(
                    text_data=json.dumps(
                        {"type": "mark_all_as_read_response", "success": True}
                    )
                )

        except json.JSONDecodeError:
            await self.send(
                text_data=json.dumps(
                    {"type": "error", "message": "Invalid JSON format"}
                )
            )

    async def notification_message(self, event):
        """إرسال إشعار جديد"""
        await self.send(
            text_data=json.dumps(
                {"type": "new_notification", "notification": event["message"]}
            )
        )

    @database_sync_to_async
    def get_unread_notifications(self):
        """الحصول على الإشعارات غير المقروءة"""
        notifications = Notification.objects.filter(
            recipient_id=self.user_id, is_read=False
        ).order_by("-created_at")[:10]

        return [
            {
                "id": n.id,
                "type": n.notification_type,
                "title": n.title,
                "message": n.message,
                "priority": n.priority,
                "created_at": n.created_at.isoformat(),
            }
            for n in notifications
        ]

    @database_sync_to_async
    def mark_notification_as_read(self, notification_id):
        """تحديد إشعار كمقروء"""
        try:
            notification = Notification.objects.get(
                id=notification_id, recipient_id=self.user_id
            )
            notification.is_read = True
            notification.read_at = timezone.now()
            notification.save()
            return True
        except Notification.DoesNotExist:
            return False

    @database_sync_to_async
    def mark_all_notifications_as_read(self):
        """تحديد جميع الإشعارات كمقروءة"""
        Notification.objects.filter(recipient_id=self.user_id, is_read=False).update(
            is_read=True, read_at=timezone.now()
        )
