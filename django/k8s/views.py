from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoModelPermissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from k8s.models import KubernetesCluster, KubernetesNamespace, KubernetesDeployment
from k8s.serializers import KubernetesClusterSerializer, KubernetesNamespaceSerializer, KubernetesDeploymentSerializer
import json
import ujson
import orjson
from k8s.utils import DateEncoder


class KubernetesClusterViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = KubernetesCluster.objects.all()
    serializer_class = KubernetesClusterSerializer

    # 列出所有
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "code": 20000,
            "data": {
                "total": len(serializer.data),
                "items": serializer.data
            }
        })


class KubernetesNamespaceViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = KubernetesNamespace.objects.all()
    serializer_class = KubernetesNamespaceSerializer

    def list(self, request, *args, **kwargs):
        cluster_name = request.query_params["cluster"]
        cluster = KubernetesCluster.objects.get(
            name=cluster_name)
        client = KubernetesNamespace.get_client(cluster_config=cluster.config)
        v1 = client.CoreV1Api()
        return Response({
            "code": 20000,
            "data": {
                "total": len(v1.list_namespace().items),
                "items": [orjson.loads(orjson.dumps(item.to_dict())) for item in v1.list_namespace().items]
            }
        })


class KubernetesNodeViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = KubernetesDeployment.objects.all()
    serializer_class = KubernetesDeploymentSerializer

    def list(self, request, *args, **kwargs):
        cluster_name = request.query_params["cluster"]
        cluster = KubernetesCluster.objects.get(
            name=cluster_name)
        client = KubernetesDeployment.get_client(cluster_config=cluster.config)
        v1 = client.CoreV1Api()
        queryset = v1.list_node().items
        return Response({
            "code": 20000,
            "data": {
                "total": len(queryset),
                "items": [orjson.loads(orjson.dumps(item.to_dict())) for item in queryset]
            }
        })


class KubernetesDeploymentViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = KubernetesDeployment.objects.all()
    serializer_class = KubernetesDeploymentSerializer

    def list(self, request, *args, **kwargs):
        cluster_name = request.query_params["cluster"]
        namespace = request.query_params["namespace"]
        cluster = KubernetesCluster.objects.get(
            name=cluster_name)
        client = KubernetesDeployment.get_client(cluster_config=cluster.config)
        v1 = client.AppsV1Api()
        queryset = v1.list_namespaced_deployment(namespace).items
        return Response({
            "code": 20000,
            "data": {
                "total": len(queryset),
                "items": [orjson.loads(orjson.dumps(item.to_dict())) for item in queryset]
            }
        })


class KubernetesDaemonSetViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = KubernetesDeployment.objects.all()
    serializer_class = KubernetesDeploymentSerializer

    def list(self, request, *args, **kwargs):
        cluster_name = request.query_params["cluster"]
        namespace = request.query_params["namespace"]
        cluster = KubernetesCluster.objects.get(
            name=cluster_name)
        client = KubernetesDeployment.get_client(cluster_config=cluster.config)
        v1 = client.AppsV1Api()
        queryset = v1.list_namespaced_daemon_set(namespace).items
        return Response({
            "code": 20000,
            "data": {
                "total": len(queryset),
                "items": [orjson.loads(orjson.dumps(item.to_dict())) for item in queryset]
            }
        })


class KubernetesStatefulSetViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = KubernetesDeployment.objects.all()
    serializer_class = KubernetesDeploymentSerializer

    def list(self, request, *args, **kwargs):
        cluster_name = request.query_params["cluster"]
        namespace = request.query_params["namespace"]
        cluster = KubernetesCluster.objects.get(
            name=cluster_name)
        client = KubernetesDeployment.get_client(cluster_config=cluster.config)
        v1 = client.AppsV1Api()
        queryset = v1.list_namespaced_stateful_set(namespace).items
        return Response({
            "code": 20000,
            "data": {
                "total": len(queryset),
                "items": [orjson.loads(orjson.dumps(item.to_dict())) for item in queryset]
            }
        })


class KubernetesPodViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = KubernetesDeployment.objects.all()
    serializer_class = KubernetesDeploymentSerializer

    def list(self, request, *args, **kwargs):
        cluster_name = request.query_params["cluster"]
        namespace = request.query_params["namespace"]
        cluster = KubernetesCluster.objects.get(
            name=cluster_name)
        client = KubernetesDeployment.get_client(cluster_config=cluster.config)
        v1 = client.CoreV1Api()
        queryset = v1.list_namespaced_pod(namespace).items
        return Response({
            "code": 20000,
            "data": {
                "total": len(queryset),
                "items": [orjson.loads(orjson.dumps(item.to_dict())) for item in queryset]
            }
        })


class KubernetesJobViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = KubernetesDeployment.objects.all()
    serializer_class = KubernetesDeploymentSerializer

    def list(self, request, *args, **kwargs):
        cluster_name = request.query_params["cluster"]
        namespace = request.query_params["namespace"]
        cluster = KubernetesCluster.objects.get(
            name=cluster_name)
        client = KubernetesDeployment.get_client(cluster_config=cluster.config)
        v1 = client.BatchV1Api()
        queryset = v1.list_namespaced_job(namespace).items
        return Response({
            "code": 20000,
            "data": {
                "total": len(queryset),
                "items": [orjson.loads(orjson.dumps(item.to_dict())) for item in queryset]
            }
        })


class KubernetesCronJobViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = KubernetesDeployment.objects.all()
    serializer_class = KubernetesDeploymentSerializer

    def list(self, request, *args, **kwargs):
        cluster_name = request.query_params["cluster"]
        namespace = request.query_params["namespace"]
        cluster = KubernetesCluster.objects.get(
            name=cluster_name)
        client = KubernetesDeployment.get_client(cluster_config=cluster.config)
        v1 = client.BatchV1beta1Api()
        queryset = v1.list_namespaced_cron_job(namespace).items
        return Response({
            "code": 20000,
            "data": {
                "total": len(queryset),
                "items": [orjson.loads(orjson.dumps(item.to_dict())) for item in queryset]
            }
        })


class KubernetesServiceViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = KubernetesDeployment.objects.all()
    serializer_class = KubernetesDeploymentSerializer

    def list(self, request, *args, **kwargs):
        cluster_name = request.query_params["cluster"]
        namespace = request.query_params["namespace"]
        cluster = KubernetesCluster.objects.get(
            name=cluster_name)
        client = KubernetesDeployment.get_client(cluster_config=cluster.config)
        v1 = client.CoreV1Api()
        queryset = v1.list_namespaced_service(namespace).items
        return Response({
            "code": 20000,
            "data": {
                "total": len(queryset),
                "items": [orjson.loads(orjson.dumps(item.to_dict())) for item in queryset]
            }
        })


class KubernetesIngressViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = KubernetesDeployment.objects.all()
    serializer_class = KubernetesDeploymentSerializer

    def list(self, request, *args, **kwargs):
        cluster_name = request.query_params["cluster"]
        namespace = request.query_params["namespace"]
        cluster = KubernetesCluster.objects.get(
            name=cluster_name)
        client = KubernetesDeployment.get_client(cluster_config=cluster.config)
        v1 = client.ExtensionsV1beta1Api()
        queryset = v1.list_namespaced_ingress(namespace).items
        return Response({
            "code": 20000,
            "data": {
                "total": len(queryset),
                "items": [orjson.loads(orjson.dumps(item.to_dict())) for item in queryset]
            }
        })


class KubernetesConfigMapViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = KubernetesDeployment.objects.all()
    serializer_class = KubernetesDeploymentSerializer

    def list(self, request, *args, **kwargs):
        cluster_name = request.query_params["cluster"]
        namespace = request.query_params["namespace"]
        cluster = KubernetesCluster.objects.get(
            name=cluster_name)
        client = KubernetesDeployment.get_client(cluster_config=cluster.config)
        v1 = client.CoreV1Api()
        queryset = v1.list_namespaced_config_map(namespace).items
        return Response({
            "code": 20000,
            "data": {
                "total": len(queryset),
                "items": [orjson.loads(orjson.dumps(item.to_dict())) for item in queryset]
            }
        })


class KubernetesSecretViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = KubernetesDeployment.objects.all()
    serializer_class = KubernetesDeploymentSerializer

    def list(self, request, *args, **kwargs):
        cluster_name = request.query_params["cluster"]
        namespace = request.query_params["namespace"]
        cluster = KubernetesCluster.objects.get(
            name=cluster_name)
        client = KubernetesDeployment.get_client(cluster_config=cluster.config)
        v1 = client.CoreV1Api()
        queryset = v1.list_namespaced_secret(namespace).items
        return Response({
            "code": 20000,
            "data": {
                "total": len(queryset),
                "items": [orjson.loads(orjson.dumps(item.to_dict())) for item in queryset]
            }
        })


class KubernetesServiceAccountViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = KubernetesDeployment.objects.all()
    serializer_class = KubernetesDeploymentSerializer

    def list(self, request, *args, **kwargs):
        cluster_name = request.query_params["cluster"]
        namespace = request.query_params["namespace"]
        cluster = KubernetesCluster.objects.get(
            name=cluster_name)
        client = KubernetesDeployment.get_client(cluster_config=cluster.config)
        v1 = client.CoreV1Api()
        queryset = v1.list_namespaced_service_account(namespace).items
        return Response({
            "code": 20000,
            "data": {
                "total": len(queryset),
                "items": [orjson.loads(orjson.dumps(item.to_dict())) for item in queryset]
            }
        })


class KubernetesRoleViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = KubernetesDeployment.objects.all()
    serializer_class = KubernetesDeploymentSerializer

    def list(self, request, *args, **kwargs):
        cluster_name = request.query_params["cluster"]
        namespace = request.query_params["namespace"]
        cluster = KubernetesCluster.objects.get(
            name=cluster_name)
        client = KubernetesDeployment.get_client(cluster_config=cluster.config)
        v1 = client.RbacAuthorizationV1Api()
        queryset = v1.list_namespaced_role(namespace).items
        return Response({
            "code": 20000,
            "data": {
                "total": len(queryset),
                "items": [orjson.loads(orjson.dumps(item.to_dict())) for item in queryset]
            }
        })


class KubernetesClusterRoleViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = KubernetesDeployment.objects.all()
    serializer_class = KubernetesDeploymentSerializer

    def list(self, request, *args, **kwargs):
        cluster_name = request.query_params["cluster"]
        cluster = KubernetesCluster.objects.get(
            name=cluster_name)
        client = KubernetesDeployment.get_client(cluster_config=cluster.config)
        v1 = client.RbacAuthorizationV1Api()
        queryset = v1.list_cluster_role().items
        return Response({
            "code": 20000,
            "data": {
                "total": len(queryset),
                "items": [orjson.loads(orjson.dumps(item.to_dict())) for item in queryset]
            }
        })


class KubernetesRoleBindingViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = KubernetesDeployment.objects.all()
    serializer_class = KubernetesDeploymentSerializer

    def list(self, request, *args, **kwargs):
        cluster_name = request.query_params["cluster"]
        namespace = request.query_params["namespace"]
        cluster = KubernetesCluster.objects.get(
            name=cluster_name)
        client = KubernetesDeployment.get_client(cluster_config=cluster.config)
        v1 = client.RbacAuthorizationV1Api()
        queryset = v1.list_namespaced_role_binding(namespace).items
        return Response({
            "code": 20000,
            "data": {
                "total": len(queryset),
                "items": [orjson.loads(orjson.dumps(item.to_dict())) for item in queryset]
            }
        })


class KubernetesClusterRoleBindingViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = KubernetesDeployment.objects.all()
    serializer_class = KubernetesDeploymentSerializer

    def list(self, request, *args, **kwargs):
        cluster_name = request.query_params["cluster"]
        cluster = KubernetesCluster.objects.get(
            name=cluster_name)
        client = KubernetesDeployment.get_client(cluster_config=cluster.config)
        v1 = client.RbacAuthorizationV1Api()
        queryset = v1.list_cluster_role_binding().items
        return Response({
            "code": 20000,
            "data": {
                "total": len(queryset),
                "items": [orjson.loads(orjson.dumps(item.to_dict())) for item in queryset]
            }
        })
