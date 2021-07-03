from rest_framework import serializers
from .models import Reviews


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ['review_id', 'user_id', 'reviewer', 'email',
                  'title', 'review_details', 'review_image', 'place_image',
                  'place_address', 'rating', 'place_id', 'place_name',
                  'admin', 'units', 'environment', 'amenities', 'createdAt']
