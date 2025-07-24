from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from .models import ChatRoom
from .serializers import ChatRoomSerializer

class GetOrCreateRoomView(APIView):
    def post(self, request):
        user1 = request.user
        user2_id = request.data.get('user2_id')
        if not user2_id:
            return Response({'error': 'user2_id required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user2 = User.objects.get(id=user2_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        room, created = ChatRoom.objects.get_or_create(user1=min(user1, user2, key=lambda u: u.id), user2=max(user1, user2, key=lambda u: u.id))
        serializer = ChatRoomSerializer(room)
        return Response(serializer.data)