from django.urls import path
from .views import GetOrCreateRoomView

urlpatterns = [
    path('room/', GetOrCreateRoomView.as_view(), name='get_or_create_room'),
]