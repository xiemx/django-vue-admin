from django.shortcuts import render
from toolkit.models import toolKitExam, toolKitIngressWhitelist, toolKitKubernetesCleaner, toolKitAutoScaling, toolKitGraphiteCleaner
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoModelPermissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from toolkit.serializers import ToolKitExamSerializer, ToolKitIngressWhitelistSerializer, ToolKitKubernetesCleanerSerializer, ToolKitAutoScalingSerializer, ToolKitGraphiteCleanerSerializer
from django.utils import timezone as datetime
from toolkit import tasks
from django.conf import settings
from common.audit_decorator import record_operation_log


class ToolKitExamViewSet(viewsets.ModelViewSet):
    """
    压测考试
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    queryset = toolKitExam.objects.all().order_by("-create_time")
    serializer_class = ToolKitExamSerializer

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)

        return Response({
            "code": 20000,
            "data": {
                "total": len(queryset),
                "items": serializer.data
            }
        })

    @record_operation_log
    def create(self, request, *args, **kwargs):
        _data = request.data
        _data["user"] = request.user.username
        _data["status"] = "ENQUEUED"

        serializer = self.get_serializer(data=_data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        res = tasks.toolkit_create_exam.delay(
            instance.id)

        return Response({
            "code": 20000,
            "message": "稍后查看任务状态，创建考试中..."
        })


class ToolKitIngressWhitelistViewSet(viewsets.ModelViewSet):
    """
    开发环境ingress 白名单更新
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    queryset = toolKitIngressWhitelist.objects.all().order_by("-create_time")
    serializer_class = ToolKitIngressWhitelistSerializer

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)

        return Response({
            "code": 20000,
            "data": {
                "total": len(queryset),
                "items": serializer.data
            }
        })

    @record_operation_log
    def create(self, request, *args, **kwargs):

        _data = request.data
        _data["user"] = request.user.username
        _data["status"] = "ENQUEUED"

        serializer = self.get_serializer(data=_data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        task_id = tasks.toolkit_update_ingress_whitelist.delay(instance.id)

        return Response({
            "code": 20000,
            "message": "稍后查看任务状态，更新 ingress whitelist 中..."
        })


class ToolKitKubernetesCleanerViewSet(viewsets.ModelViewSet):
    """
    K8S 被驱逐 pod 清理。
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    queryset = toolKitKubernetesCleaner.objects.all().order_by("-create_time")
    serializer_class = ToolKitKubernetesCleanerSerializer

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)

        return Response({
            "code": 20000,
            "data": {
                "total": len(queryset),
                "items": serializer.data
            }
        })

    @record_operation_log
    def create(self, request, *args, **kwargs):

        _data = request.data
        _data["user"] = request.user.username
        _data["status"] = "ENQUEUED"

        serializer = self.get_serializer(data=_data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        task_id = tasks.toolkit_clean_evicted_pod.delay(
            cluster=_data["cluster"], task_id=instance.id)

        return Response({"code": 20000, "message": "job is enqueued."})


class ToolKitAutoScalingViewSet(viewsets.ModelViewSet):
    """
    扩缩容服务
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    queryset = toolKitAutoScaling.objects.all().order_by("-id")
    serializer_class = ToolKitAutoScalingSerializer

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)

        return Response({
            "code": 20000,
            "data": {
                "total": len(queryset),
                "items": serializer.data
            }
        })

    @record_operation_log
    def create(self, request, *args, **kwargs):

        _data = request.data
        _data["user"] = request.user.username
        _data["status"] = "ENQUEUED"

        serializer = self.get_serializer(data=_data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        task_id = tasks.toolkit_autoscaling_service.delay(task_id=instance.id)

        return Response({"code": 20000, "message": "job is enqueued."})


class ToolKitGraphiteCleanerViewSet(viewsets.ModelViewSet):
    """
    开发环境ingress 白名单更新
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    queryset = toolKitGraphiteCleaner.objects.all().order_by("-id")
    serializer_class = ToolKitGraphiteCleanerSerializer

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)

        return Response({
            "code": 20000,
            "data": {
                "total": len(queryset),
                "items": serializer.data
            }
        })

    @record_operation_log
    def create(self, request, *args, **kwargs):

        _data = request.data
        _data["user"] = request.user.username
        _data["status"] = "ENQUEUED"

        serializer = self.get_serializer(data=_data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()
        task_id = tasks.toolkit_graphite_cleaner.delay(instance.id)

        return Response({
            "code": 20000,
            "message": "稍后查看任务状态，清理 Graphite disk 任务进行中..."
        })
