from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Like
from .serializers import LikeSerializer
from django.shortcuts import get_object_or_404

class LikePostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        """
        Like a post by current user.
        """
        like, created = Like.objects.get_or_create(user=request.user, post_id=post_id)
        if created:
            serializer = LikeSerializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'You already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        """
        Unlike a post by current user.
        """
        like = Like.objects.filter(user=request.user, post_id=post_id).first()
        if not like:
            return Response({'detail': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        return Response({'detail': 'Unliked successfully.'}, status=status.HTTP_204_NO_CONTENT)
