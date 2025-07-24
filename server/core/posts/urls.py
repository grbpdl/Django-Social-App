from django.urls import path
from .views import UserPostListCreateAPIView, UserPostRetrieveUpdateDestroyAPIView,AllPostsListAPIView

urlpatterns = [
    path('', UserPostListCreateAPIView.as_view(), name='user-posts-list-create'),
    path('<int:pk>/', UserPostRetrieveUpdateDestroyAPIView.as_view(), name='user-post-detail'),
     path('all/', AllPostsListAPIView.as_view(), name='all-posts-list'),
]
