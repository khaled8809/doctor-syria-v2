"""
WebSocket consumers for doctor_syria project.
"""

import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone


class BaseConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        await self.process_message(text_data_json)

    async def process_message(self, data):
        raise NotImplementedError("Subclasses must implement process_message")


class NotificationConsumer(BaseConsumer):
    async def connect(self):
        await super().connect()
        await self.channel_layer.group_add(
            f"user_{self.scope['user'].id}_notifications", self.channel_name
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"user_{self.scope['user'].id}_notifications", self.channel_name
        )

    async def notification(self, event):
        await self.send(
            text_data=json.dumps({"type": "notification", "message": event["message"]})
        )


class ChatConsumer(BaseConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await super().connect()
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def process_message(self, data):
        message = data["message"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": self.scope["user"].username,
                "timestamp": timezone.now().isoformat(),
            },
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "chat",
                    "message": event["message"],
                    "user": event["user"],
                    "timestamp": event["timestamp"],
                }
            )
        )


class AppointmentStatusConsumer(BaseConsumer):
    async def connect(self):
        await super().connect()
        await self.channel_layer.group_add("appointment_updates", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("appointment_updates", self.channel_name)

    async def appointment_update(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "appointment_update",
                    "appointment_id": event["appointment_id"],
                    "status": event["status"],
                    "message": event["message"],
                }
            )
        )


class LiveDashboardConsumer(BaseConsumer):
    async def connect(self):
        if not self.scope["user"].is_staff:
            await self.close()
            return

        await super().connect()
        await self.channel_layer.group_add("live_dashboard", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("live_dashboard", self.channel_name)

    async def dashboard_update(self, event):
        await self.send(
            text_data=json.dumps({"type": "dashboard_update", "data": event["data"]})
        )
