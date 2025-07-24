from rest_framework import serializers
from django.core.mail import send_mail
import random
from .models import User, Follower, PasswordResetOTP

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'full_name',
            'profile_picture',
            'is_premium',
            'password',
            'followers',
            'following',
            'follower_count','following_count',
            'created_at',
        ]
        read_only_fields = ['is_premium', 'created_at']

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        if request and request.user and request.user.is_staff:
            fields['is_premium'].read_only = False
        return fields

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
    def get_followers(self, obj):
        followers = Follower.objects.filter(following=obj)
        return FollowerSerializer(followers, many=True).data

    def get_following(self, obj):
        following = Follower.objects.filter(follower=obj)
        return FollowerSerializer(following, many=True).data
    
    def get_follower_count(self, obj):
        return Follower.objects.filter(following=obj).count()

    def get_following_count(self, obj):
        return Follower.objects.filter(follower=obj).count()
    

class FollowerSerializer(serializers.ModelSerializer):
    follower_username = serializers.CharField(source='follower.username', read_only=True)
    following_username = serializers.CharField(source='following.username', read_only=True)


    class Meta:
        model = Follower
        fields = ['id', 'follower', 'follower_username', 'following', 'following_username', 'created_at']


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data['email']
        otp = data['otp']
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("User not found.")
        otp_obj = PasswordResetOTP.objects.filter(user=user, otp=otp).order_by('-created_at').first()
        if not otp_obj or otp_obj.is_expired():
            raise serializers.ValidationError("Invalid or expired OTP.")
        return data

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.set_password(self.validated_data['new_password'])
        user.save()
        PasswordResetOTP.objects.filter(user=user).delete()

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'is_staff', 'is_premium']
        read_only_fields = ['id', 'username', 'email']
