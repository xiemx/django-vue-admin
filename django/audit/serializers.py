from rest_framework import serializers
from django.contrib.auth.models import User
from audit.models import UserOperationLog


class UserOperationLogSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = UserOperationLog
        fields = "__all__"
