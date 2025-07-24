from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Comment, Post
from .serializers import CommentSerializer
from accounts.permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404

# 1. Create a comment on a specific post
class CommentCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        # Ensure the post exists
        post = get_object_or_404(Post, id=post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2 & 3. Edit or Delete a comment
class CommentEditDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Comment, pk=pk)

    def put(self, request, pk):
        comment = self.get_object(pk)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        comment = self.get_object(pk)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = self.get_object(pk)

        # Allow comment owner or the post owner
        is_comment_owner = comment.user == request.user
        is_post_owner = comment.post.user == request.user

        if not (is_comment_owner or is_post_owner):
            return Response({"detail": "You do not have permission to delete this comment."}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

