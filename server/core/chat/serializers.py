from rest_framework import serializers

from .models import ChatRoom, ChatMessage

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'user1', 'user2', 'room_name']

class ChatMessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    class Meta:
        model = ChatMessage
        fields = ['id', 'room', 'sender', 'sender_username', 'message', 'timestamp', 'is_read']