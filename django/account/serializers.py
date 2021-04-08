from django.contrib.auth.models import User, Group, Permission
from rest_framework import serializers
from user_profile.serializers import UserProfileSerializer


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    groups = serializers.SlugRelatedField(
        many=True,
        queryset=Group.objects.all(),
        slug_field='name'
    )
    profile = UserProfileSerializer(allow_null=True)

    # def to_representation(self, value):
    #     data = super().to_representation(value)
    #     data['profile'] = {}
    #     return data

    class Meta:
        model = User
        # fields = "__all__"
        fields = ['id', 'username', 'groups', 'last_login', 'is_superuser',
                  'email', 'is_staff', 'is_active', 'profile']
        extra_kwargs = {
            'password': {'allow_null': True, 'allow_blank': True}
        }  # 指定序列化字段属性


class PermsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ('id', 'url', 'name')


class GroupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    permissions = serializers.SlugRelatedField(
        many=True,
        queryset=Permission.objects.all(),
        slug_field='name'
    )

    # 增加自定义属性
    def to_representation(self, value):
        data = super().to_representation(value)
        data['users'] = [i.username for i in value.user_set.all()]

        return data

    class Meta:
        model = Group
        fields = "__all__"
