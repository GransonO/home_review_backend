from rest_framework import serializers
from .models import Support


class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = ['support_id', 'user_id', 'email',
                  'title', 'details', 'photo', 'tracker',
                  'response', 'createdAt', 'updatedAt']
