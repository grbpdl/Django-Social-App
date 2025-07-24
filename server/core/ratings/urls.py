from django.urls import path
from .views import RatePostAPIView

urlpatterns = [
    path('posts/<int:post_id>/rate/', RatePostAPIView.as_view(), name='rate-post'),
    # path('posts/<int:post_id>/ratings/', PostRatingsListAPIView.as_view(), name='ratings-list'),
]
