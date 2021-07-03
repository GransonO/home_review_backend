from rest_framework import serializers
from .models import Homes


class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homes
        fields = ['home_id', 'user_id', 'description',
                  'administrator', 'bathrooms', 'bedrooms', 'place_id',
                  'place_image', 'address', 'name', 'createdAt', 'updatedAt']
