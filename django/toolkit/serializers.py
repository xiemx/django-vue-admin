from rest_framework import serializers
from toolkit.models import toolKitExam, toolKitIngressWhitelist, toolKitKubernetesCleaner, toolKitAutoScaling, toolKitGraphiteCleaner
from django.contrib.auth.models import User
from k8s.models import KubernetesCluster


class ToolKitExamSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = toolKitExam
        fields = "__all__"


class ToolKitIngressWhitelistSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = toolKitIngressWhitelist
        fields = "__all__"


class ToolKitKubernetesCleanerSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    cluster = serializers.SlugRelatedField(
        queryset=KubernetesCluster.objects.all(),
        slug_field='name'
    )

    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = toolKitKubernetesCleaner
        fields = "__all__"


class ToolKitAutoScalingSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = toolKitAutoScaling
        fields = "__all__"


class ToolKitGraphiteCleanerSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = toolKitGraphiteCleaner
        fields = "__all__"
