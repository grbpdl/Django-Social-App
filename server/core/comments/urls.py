from django.urls import path
from .views import CommentCreateAPIView, CommentEditDeleteAPIView

urlpatterns = [
    path('posts/<int:post_id>/comments/', CommentCreateAPIView.as_view(), name='create-comment'),
    path('<int:pk>/', CommentEditDeleteAPIView.as_view(), name='edit-delete-comment'),
]
