from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Rating
from .serializers import RatingSerializer
from django.shortcuts import get_object_or_404

class RatePostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        rating_value = request.data.get("rating_value")
        if not rating_value:
            return Response({"detail": "Rating value is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Create or update rating
        rating, created = Rating.objects.update_or_create(
            user=request.user,
            post_id=post_id,
            defaults={'rating_value': rating_value}
        )
        serializer = RatingSerializer(rating)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    def delete(self, request, post_id):
        rating = Rating.objects.filter(user=request.user, post_id=post_id).first()
        if not rating:
            return Response({"detail": "You haven't rated this post."}, status=status.HTTP_400_BAD_REQUEST)
        rating.delete()
        return Response({"detail": "Rating removed."}, status=status.HTTP_204_NO_CONTENT)
