from django.urls import path
from .views import (
    UserPostListCreateAPIView, 
    UserPostRetrieveUpdateDestroyAPIView,
    AllPostsListAPIView,
    CategoryListCreateAPIView,
    SavedPostListAPIView,
    SavePostAPIView,
    UnsavePostAPIView
)

urlpatterns = [
    path('', UserPostListCreateAPIView.as_view(), name='user-posts-list-create'),
    path('<int:pk>/', UserPostRetrieveUpdateDestroyAPIView.as_view(), name='user-post-detail'),
    path('all/', AllPostsListAPIView.as_view(), name='all-posts-list'),
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('saved/', SavedPostListAPIView.as_view(), name='saved-posts-list'),
    path('save/<int:post_id>/', SavePostAPIView.as_view(), name='save-post'),
    path('unsave/<int:post_id>/', UnsavePostAPIView.as_view(), name='unsave-post'),
]
