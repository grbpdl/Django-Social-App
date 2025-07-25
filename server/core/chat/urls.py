from django.urls import path
from .views import GetOrCreateRoomView, ChatRoomMessagesView

urlpatterns = [
    path('room/', GetOrCreateRoomView.as_view(), name='get_or_create_room'),
    path('room/<str:room_name>/messages/', ChatRoomMessagesView.as_view(), name='chat_room_messages'),
]