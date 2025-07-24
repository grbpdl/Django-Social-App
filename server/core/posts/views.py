from rest_framework.views import APIView
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Post
from .serializers import PostSerializer
from rest_framework.permissions import AllowAny 
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter
from accounts.models import Follower
from django.db.models import Avg, Q


class UserPostListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # List posts only from the logged-in user
        posts = Post.objects.filter(user=request.user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Create post by logged-in user
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPostRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        post = self.get_object(pk, request.user)
        if not post:
             Response({"detail": "Not found or not your post"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data)


    def get_object(self, pk, user):
        try:
            return Post.objects.get(pk=pk, user=user)
        except Post.DoesNotExist:
            return None

    def put(self, request, pk):
        post = self.get_object(pk, request.user)
        if not post:
            return Response({"detail": "Not found or not your post"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save(user=request.user)  # user remains the same
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        post = self.get_object(pk, request.user)
        if not post:
            return Response({"detail": "Not found or not your post"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk, request.user)
        if not post:
            return Response({"detail": "Not found or not your post"}, status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class PostFilter(FilterSet):
    min_rating = NumberFilter(method='filter_min_rating')
    max_rating = NumberFilter(method='filter_max_rating')

    class Meta:
        model = Post
        fields = ['category']  # default category filter

    def filter_min_rating(self, queryset, name, value):
        return queryset.annotate(avg_rating=Avg('ratings__rating_value')).filter(avg_rating__gte=value)

    def filter_max_rating(self, queryset, name, value):
        return queryset.annotate(avg_rating=Avg('ratings__rating_value')).filter(avg_rating__lte=value)


class AllPostsListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PostFilter
    search_fields = ['content']
    ordering_fields = ['created_at', 'avg_rating'] 
    ordering = ['-created_at']

    def get_queryset(self):
        base_queryset = Post.objects.all().annotate(avg_rating=Avg('ratings__rating_value'))

        user = self.request.user
        if user.is_authenticated:
            # Get the IDs of users the current user is following
            following_ids = Follower.objects.filter(follower=user).values_list('following_id', flat=True)

            # Annotate whether post author is followed
            return base_queryset.annotate(
                is_followed=Q(user__in=following_ids)
            ).order_by(
                '-is_followed', '-created_at'
            )

        # For unauthenticated users: return default sorted by created_at
        return base_queryset.order_by('-created_at')