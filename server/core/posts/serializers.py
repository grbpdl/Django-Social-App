from rest_framework import serializers
from .models import Post, PostCategory
from likes.serializers import LikeSerializer
from comments.serializers import CommentSerializer
from ratings.models import Rating  # adjust path if needed
from django.db.models import Avg

class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ['id', 'name']

class PostSerializer(serializers.ModelSerializer):
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