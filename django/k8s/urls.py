from django.conf.urls import url, include
from rest_framework import routers

from k8s.views import (
    KubernetesClusterViewSet,
    KubernetesNamespaceViewSet,
    KubernetesDeploymentViewSet,
    KubernetesDaemonSetViewSet,
    KubernetesStatefulSetViewSet,
    KubernetesPodViewSet,
    KubernetesCronJobViewSet,
    KubernetesJobViewSet,
    KubernetesIngressViewSet,
    KubernetesServiceViewSet,
    KubernetesServiceAccountViewSet,
    KubernetesRoleViewSet,
    KubernetesClusterRoleViewSet,
    KubernetesRoleBindingViewSet,
    KubernetesClusterRoleViewSet,
    KubernetesClusterRoleBindingViewSet,
    KubernetesConfigMapViewSet,
    KubernetesSecretViewSet,
    KubernetesNodeViewSet
)


router = routers.DefaultRouter()
router.register(r'cluster', KubernetesClusterViewSet)
router.register(r'node', KubernetesNodeViewSet)
router.register(r'namespace', KubernetesNamespaceViewSet)
router.register(r'deployment', KubernetesDeploymentViewSet)
router.register(r'daemonset', KubernetesDaemonSetViewSet)
router.register(r'statefulset', KubernetesStatefulSetViewSet)
router.register(r'pod', KubernetesPodViewSet)
router.register(r'cronjob', KubernetesCronJobViewSet)
router.register(r'job', KubernetesJobViewSet)
router.register(r'ingress', KubernetesIngressViewSet)
router.register(r'service', KubernetesServiceViewSet)
router.register(r'service-account', KubernetesServiceAccountViewSet)
router.register(r'role', KubernetesRoleViewSet)
router.register(r'role-binding', KubernetesRoleBindingViewSet)
router.register(r'cluster-role', KubernetesClusterRoleViewSet)
router.register(r'cluster-role-binding',
                KubernetesClusterRoleBindingViewSet)
router.register(r'configmap', KubernetesConfigMapViewSet)
router.register(r'secret', KubernetesSecretViewSet)

urlpatterns = [
    url('', include(router.urls)),
]
