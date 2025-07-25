
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.models import User
from .models import ChatRoom
from .serializers import ChatRoomSerializer, ChatMessageSerializer
from rest_framework.permissions import IsAuthenticated
class ChatRoomMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_name):
        from .models import ChatRoom, ChatMessage
        try:
            room = ChatRoom.objects.get(room_name=room_name)
        except ChatRoom.DoesNotExist:
            return Response({'error': 'Chat room does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        messages = ChatMessage.objects.filter(room=room).order_by('timestamp')
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

class GetOrCreateRoomView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user1 = request.user
        user2_id = request.data.get('user2_id')
        if not user2_id:
            return Response({'error': 'user2_id required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user2 = User.objects.get(id=user2_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        # Check if both users are premium
        if not getattr(user1, 'is_premium', False) or not getattr(user2, 'is_premium', False):
            return Response({'error': 'Both users must be premium to initiate chat.'}, status=status.HTTP_403_FORBIDDEN)
        room, created = ChatRoom.objects.get_or_create(user1=min(user1, user2, key=lambda u: u.id), user2=max(user1, user2, key=lambda u: u.id))
        serializer = ChatRoomSerializer(room)
        return Response(serializer.data)

class MarkMessagesReadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, room_name):
        from .models import ChatRoom, ChatMessage
        try:
            room = ChatRoom.objects.get(room_name=room_name)
        except ChatRoom.DoesNotExist:
            return Response({'error': 'Chat room does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        # Mark all messages in this room as read for the current user (not sent by the user)
        updated = ChatMessage.objects.filter(room=room, is_read=False).exclude(sender=request.user).update(is_read=True)
        return Response({'marked_read': updated})
