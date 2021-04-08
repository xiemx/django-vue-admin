from rest_framework import serializers
from k8s.models import KubernetesCluster, KubernetesNamespace, KubernetesDeployment


class KubernetesClusterSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = KubernetesCluster
        fields = "__all__"


class KubernetesNamespaceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = KubernetesNamespace
        fields = "__all__"


class KubernetesDeploymentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = KubernetesDeployment
        fields = "__all__"
