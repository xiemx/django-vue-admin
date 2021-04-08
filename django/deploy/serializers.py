from rest_framework import serializers
from account.serializers import UserSerializer
from deploy.models import Service, Release
from k8s.models import KubernetesCluster
from django.contrib.auth.models import User


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Service
        fields = "__all__"


class ReleaseSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )
    cluster = serializers.SlugRelatedField(
        queryset=KubernetesCluster.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Release
        fields = "__all__"
