from rest_framework import serializers
from .models import Rating

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'post', 'rating_value', 'created_at']
        read_only_fields = ['user', 'post', 'created_at']
