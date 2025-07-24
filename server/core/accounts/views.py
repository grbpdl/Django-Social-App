from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import PasswordResetOTP, User, Follower
from .serializers import (
    UserSerializer, FollowerSerializer,
    ForgotPasswordSerializer, ResetPasswordSerializer,
    AdminUserSerializer
)
from .permissions import IsOwnerOrReadOnly, IsAdminUserOrReadOnly,IsUserOrAdmin
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
import random

# User-related APIViews
class UserRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # Generate token pair for the newly registered user
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            return Response({
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(access)
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserListView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class GetMyInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsUserOrAdmin]

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        
        # Enforce object-level permissions
        self.check_object_permissions(request, user)
        
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsUserOrAdmin]

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDeleteView(APIView):
    permission_classes = [permissions.IsAdminUser]  # Stricter: only admins can delete

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Follower-related APIViews
class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            to_follow = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if to_follow == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        follower_obj, created = Follower.objects.get_or_create(
            follower=request.user, following=to_follow
        )

        if not created:
            return Response({"detail": "You are already following this user."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = FollowerSerializer(follower_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, user_id):
        try:
            to_unfollow = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            follow_obj = Follower.objects.get(follower=request.user, following=to_unfollow)
        except Follower.DoesNotExist:
            return Response({"detail": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)

        follow_obj.delete()
        return Response({"detail": "Unfollowed successfully."}, status=status.HTTP_204_NO_CONTENT)


class MyFollowersListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        followers = Follower.objects.filter(following=request.user)
        serializer = FollowerSerializer(followers, many=True)
        return Response(serializer.data)


class MyFollowingListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        following = Follower.objects.filter(follower=request.user)
        serializer = FollowerSerializer(following, many=True)
        return Response(serializer.data)
# Admin User-related APIViews
class AdminUserListView(APIView):
    permission_classes = [IsAdminUserOrReadOnly]

    def get(self, request):
        users = User.objects.all()
        serializer = AdminUserSerializer(users, many=True)
        return Response(serializer.data)

class AdminUserDetailView(APIView):
    permission_classes = [IsAdminUserOrReadOnly]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = AdminUserSerializer(user)
        return Response(serializer.data)




class AdminUserDeleteView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AdminUserPromotePremiumView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if user.is_premium:
            return Response({"message": f"{user.username} is already a premium user."}, status=status.HTTP_200_OK)
        
        user.is_premium = True
        user.save()
        serializer = AdminUserSerializer(user)
        return Response({
            "message": f"{user.username} is now a premium user.",
            "user": serializer.data
        }, status=status.HTTP_200_OK)

class AdminUserDemotePremiumView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        user.is_premium = False
        user.save()
        serializer = AdminUserSerializer(user)
        return Response({"message": f"{user.username} is no longer a premium user.", "user": serializer.data})

#forgot password and reset password views


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            otp = str(random.randint(100000, 999999))

            # Save OTP to DB
            PasswordResetOTP.objects.create(user=user, otp=otp)

            # Send OTP via email
            try:
                send_mail(
                    'Password Reset OTP',
                    f'Your OTP for resetting your password is: {otp}',
                    'paudyal.gaurab11@gmail.com',
                    [email],
                    fail_silently=False,
                )
                return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": "Failed to send OTP. Try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)