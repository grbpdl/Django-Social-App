from rest_framework import serializers
from .models import Post, PostCategory, SavedPost

from accounts.serializers import UserSerializer
from likes.serializers import LikeSerializer
from comments.serializers import CommentSerializer
from ratings.models import Rating  # adjust path if needed
from django.db.models import Avg

class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ['id', 'name']


class PostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSerializer.Meta.model
        fields = ['id', 'username', 'full_name', 'profile_picture']

class PostSerializer(serializers.ModelSerializer):
    user = PostUserSerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=PostCategory.objects.all())
    likes = LikeSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [f.name for f in Post._meta.get_fields() if not f.is_relation or f.one_to_one or (f.many_to_one and f.related_model)] + ['likes', 'comments', 'average_rating']
        read_only_fields = ['user']

    def get_average_rating(self, obj):
        avg = obj.ratings.aggregate(avg_rating=Avg('rating_value'))['avg_rating']
        return round(avg, 2) if avg is not None else 0.0
    
class SavedPostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    post = PostSerializer(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), source='post', write_only=True)

    class Meta:
        model = SavedPost
        fields = ['id', 'user', 'post', 'post_id', 'saved_at']
        read_only_fields = ['id', 'user', 'post', 'saved_at']