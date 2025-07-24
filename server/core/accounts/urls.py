from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    UserRegisterView, UserListView, UserDetailView, UserUpdateView, UserDeleteView,GetMyInfoView,
   FollowUserView,
    UnfollowUserView,
    MyFollowersListView,
    MyFollowingListView,
    AdminUserListView, UserRegisterView, AdminUserDetailView, UserUpdateView,
    AdminUserDeleteView, AdminUserPromotePremiumView, AdminUserDemotePremiumView,
    ForgotPasswordView, ResetPasswordView
)

urlpatterns = [
    # User endpoints
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/register/', UserRegisterView.as_view(), name='user-register'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('me/', GetMyInfoView.as_view(), name='get-my-info'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    
    # Follower endpoints
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('followers/', MyFollowersListView.as_view(), name='my-followers'),
    path('following/', MyFollowingListView.as_view(), name='my-following'),
    
    # Admin user endpoints
    path('admin/users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('admin/users/create/', UserRegisterView.as_view(), name='admin-user-create'),
    path('admin/users/<int:pk>/', AdminUserDetailView.as_view(), name='admin-user-detail'),
    path('admin/users/<int:pk>/update/', UserUpdateView.as_view(), name='admin-user-update'),
    path('admin/users/<int:pk>/delete/', AdminUserDeleteView.as_view(), name='admin-user-delete'),
    path('admin/users/<int:pk>/promote_premium/', AdminUserPromotePremiumView.as_view(), name='admin-user-promote-premium'),
    path('admin/users/<int:pk>/demote_premium/', AdminUserDemotePremiumView.as_view(), name='admin-user-demote-premium'),
    
    # Authentication and password reset endpoints
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]