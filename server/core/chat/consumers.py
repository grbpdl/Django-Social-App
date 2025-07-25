
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = None
        self.room_group_name = None
        user = self.scope.get('user')
        if not user or not user.is_authenticated or not getattr(user, 'is_premium', False):
            await self.close(code=4001)
            return
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name') and self.room_group_name:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        from django.contrib.auth import get_user_model
        from .models import ChatRoom, ChatMessage
        data = json.loads(text_data)
        message = data['message']
        user = self.scope.get('user')
        # Persist message to DB
        try:
            room = await self.get_room(self.room_name)
        except ChatRoom.DoesNotExist:
            # Auto-create the chat room if it does not exist
            user_ids = self.room_name.replace('room_', '').split('_')
            if len(user_ids) == 2:
                user1_id, user2_id = int(user_ids[0]), int(user_ids[1])
                User = get_user_model()
                user1 = await self.get_user_by_id(user1_id)
                user2 = await self.get_user_by_id(user2_id)
                if not (user1 and user2):
                    await self.send(text_data=json.dumps({'error': 'Invalid user IDs for chat room.'}))
                    return
                # Check if both users are premium
                if not (getattr(user1, 'is_premium', False) and getattr(user2, 'is_premium', False)):
                    await self.send(text_data=json.dumps({'error': 'Both users must be premium to initiate chat.'}))
                    return
                room = await self.create_room(user1, user2)
            else:
                await self.send(text_data=json.dumps({'error': 'Invalid room name format.'}))
                return
        try:
            await self.create_message(room, user, message)
        except Exception as e:
            await self.send(text_data=json.dumps({'error': 'Failed to save message', 'details': str(e)}))
            return
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': user.username if user else None
            }
        )

    @database_sync_to_async
    def get_user_by_id(self, user_id):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def create_room(self, user1, user2):
        from .models import ChatRoom
        return ChatRoom.objects.create(user1=min(user1, user2, key=lambda u: u.id), user2=max(user1, user2, key=lambda u: u.id))

    @database_sync_to_async
    def get_room(self, room_name):
        from .models import ChatRoom
        return ChatRoom.objects.get(room_name=room_name)

    @database_sync_to_async
    def create_message(self, room, user, message):
        from .models import ChatMessage
        return ChatMessage.objects.create(room=room, sender=user, message=message)

    async def chat_message(self, event):
        message = event['message']
        sender = event.get('sender')
        await self.send(text_data=json.dumps({'message': message, 'sender': sender}))
