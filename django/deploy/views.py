from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoModelPermissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from deploy.models import Service, Release
from deploy.serializers import ServiceSerializer, ReleaseSerializer
import json
import subprocess
from k8s.models import KubernetesCluster
from tempfile import NamedTemporaryFile

from deploy.tasks import DeployService
from deploy.utils import exec_helm_command
from common.audit_decorator import record_operation_log


class ServiceViewSet(viewsets.ModelViewSet):

    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = Service.objects.all().order_by("-id")
    serializer_class = ServiceSerializer

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

    @record_operation_log
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "code": 20000,
            "message": "create service success."
        })

    @record_operation_log
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response({
            "code": 20000,
            "message": "update service success."
        })

    @record_operation_log
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "code": 20000,
            "message": "delete service success."
        })


class ReleaseViewSet(viewsets.ModelViewSet):

    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = Release.objects.all().order_by("-id")
    serializer_class = ReleaseSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against query parameter in the URL.
        """
        queryset = Release.objects.all().order_by("-id")

        _filter_kwargs = {}

        cluster = self.request.query_params.get('cluster', None)
        user = self.request.query_params.get('user', None)
        service = self.request.query_params.get('service', None)
        namespace = self.request.query_params.get('namespace', None)
        task_id = self.request.query_params.get('task_id', None)
        time_range = self.request.query_params.getlist('time_range[]', None)

        if cluster:
            _filter_kwargs['cluster__name'] = cluster

        if user:
            _filter_kwargs['user__username'] = user

        if service:
            _filter_kwargs['service'] = service

        if namespace:
            _filter_kwargs['namespace'] = namespace

        if task_id:
            _filter_kwargs['task_id'] = task_id

        if time_range:
            _filter_kwargs['create_time__gte'] = time_range[0]
            _filter_kwargs['create_time__lte'] = time_range[-1]

        if _filter_kwargs:
            queryset = queryset.filter(**_filter_kwargs).order_by("-id")

        return queryset

    def list(self, request, *args, **kwargs):
        _type = request.query_params.get('type', None)
        cluster_name = request.query_params.get('cluster', None)
        namespace = request.query_params.get("namespace", None)

        if _type == "current":
            _command = 'helm list -o json -a --namespace {}'.format(
                namespace)
            code, output = exec_helm_command(cluster_name, _command)
            _content = {
                "code": 20000,
                "data": {
                    "total": len(json.loads(output)),
                    "items": json.loads(output)
                }}

        elif _type == "history":
            service = request.query_params.get("service", None)

            if not service:
                raise Exception("Service name required to get history.")

            _command = "helm history {} -o json --namespace {}".format(
                service, namespace)

            code, output = exec_helm_command(cluster_name, _command)
            _content = {
                "code": 20000,
                "data": {
                    "total": len(json.loads(output)),
                    "items": json.loads(output)
                }}

        else:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)

            else:
                serializer = self.get_serializer(queryset, many=True)
            _content = {
                "code": 20000,
                "data": {
                    "total": len(queryset),
                    "items": serializer.data
                }
            }

        return Response(_content)

    @record_operation_log
    def create(self, request, *args, **kwargs):

        _data = request.data
        _data["user"] = request.user.username

        serializer = self.get_serializer(data=_data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        try:

            _task_id = DeployService.delay(instance.id)

        except Exception as err:
            instance.status = "FAILURE"
            instance.save()
            print(err)
            return Response({
                "code": 20001,
                "message": "创建任务失败。"
            })
        else:
            instance.status = "ENQUEUED"
            instance.task_id = _task_id
            instance.save()
            return Response({
                "code": 20000,
                "message": "稍后查看发布状态, equeued..."
            })
