from rest_framework import serializers
from django.contrib.auth.models import User
from user_profile.models import profile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = profile
        fields = ['avatar', 'alicloud', 'dingding', 'phone']
