from django.urls import path
from .views import LikePostAPIView

urlpatterns = [
    path('posts/<int:post_id>/like/', LikePostAPIView.as_view(), name='like-unlike-post')
]
