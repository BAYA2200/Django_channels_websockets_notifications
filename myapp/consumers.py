import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'notifications'

        # Присоединяемся к группе уведомлений
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Отключаемся от группы
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Обработка уведомления
    async def send_notification(self, event):
        message = event['message']

        # Отправляем уведомление обратно клиентам
        await self.send(text_data=json.dumps({
            'message': message
        }))
