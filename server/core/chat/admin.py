from django.contrib import admin
from .models import ChatRoom, ChatMessage

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['room_name', 'user1', 'user2']
    search_fields = ['room_name', 'user1__username', 'user2__username']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'room', 'message', 'timestamp', 'is_read']
    list_filter = ['is_read', 'timestamp']
    search_fields = ['message', 'sender__username']
