import json
from channels.generic.websocket import AsyncWebsocketConsumer

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatMessage

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]
        self.other_user_id = self.scope['url_route']['kwargs']['user_id']

        if not self.user.is_authenticated:
            await self.close()
            return

        # To create a unique room name for the two users (sort ids to avoid duplication)
        users = sorted([str(self.user.id), self.other_user_id])
        self.room_group_name = f'chat_{users[0]}_{users[1]}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '').strip()

        if message:
            # Save message in DB
            chat_message = await self.save_message(self.user.id, int(self.other_user_id), message)

            # Broadcast message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': chat_message.message,
                    'sender_id': chat_message.sender.id,
                    'receiver_id': chat_message.receiver.id,
                    'timestamp': chat_message.timestamp.isoformat(),
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, message):
        return ChatMessage.objects.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            message=message
        )
