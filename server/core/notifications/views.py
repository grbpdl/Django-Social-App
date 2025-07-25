# API view to mark a notification as read
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response


from rest_framework import generics

# API view to push notifications
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Notification
from .serializers import NotificationSerializer
from accounts.models import User

class PushNotificationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_id = request.data.get('user')
        message = request.data.get('message')
        if not user_id or not message:
            return Response({'error': 'user and message are required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        notification = Notification.objects.create(user=user, message=message)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# List notifications for the authenticated user
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

class MarkNotificationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, user=request.user)
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found.'}, status=status.HTTP_404_NOT_FOUND)
        notification.is_read = True
        notification.save()
        serializer = NotificationSerializer(notification)
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({
            'notification': serializer.data,
            'unread_count': unread_count
        }, status=status.HTTP_200_OK)