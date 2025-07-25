from django.urls import path
from .views import GetOrCreateRoomView, ChatRoomMessagesView, MarkMessagesReadView

urlpatterns = [
    path('room/', GetOrCreateRoomView.as_view(), name='get_or_create_room'),
    path('room/<str:room_name>/messages/', ChatRoomMessagesView.as_view(), name='chat_room_messages'),
    path('room/<str:room_name>/mark_read/', MarkMessagesReadView.as_view(), name='chat_room_mark_read'),
]