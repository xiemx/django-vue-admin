from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoModelPermissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django_celery_beat.models import (
    IntervalSchedule,
    SolarSchedule,
    CrontabSchedule,
    ClockedSchedule,
    PeriodicTask
)

from job.serializers import (
    IntervalScheduleSerializer,
    SolarScheduleSerializer,
    ClockedScheduleSerializer,
    CrontabScheduleSerializer,
    PeriodicTaskSerializer,
    TaskResultSerializer
)

from django_celery_results.models import TaskResult
from common.audit_decorator import record_operation_log


class IntervalScheduleViewSet(viewsets.ModelViewSet):

    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions, )

    queryset = IntervalSchedule.objects.all().order_by("-id")
    serializer_class = IntervalScheduleSerializer

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
            "message": "create schedule success."
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
            "message": "update schedule success."
        })

    @record_operation_log
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "code": 20000,
            "message": "delete schedule success."
        })


class SolarScheduleViewSet(viewsets.ModelViewSet):

    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions, )

    queryset = SolarSchedule.objects.all().order_by("-id")
    serializer_class = SolarScheduleSerializer

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
            "message": "create schedule success."
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
            "message": "update schedule success."
        })

    @record_operation_log
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "code": 20000,
            "message": "delete schedule success."
        })


class CrontabScheduleViewSet(viewsets.ModelViewSet):

    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions, )

    queryset = CrontabSchedule.objects.all().order_by("-id")
    serializer_class = CrontabScheduleSerializer

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
            "message": "create schedule success."
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
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({
            "code": 20000,
            "message": "update schedule success."
        })

    @record_operation_log
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "code": 20000,
            "message": "delete schedule success."
        })


class ClockedScheduleViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions, )

    queryset = ClockedSchedule.objects.all().order_by("-id")
    serializer_class = ClockedScheduleSerializer

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
            "message": "create schedule success."
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
            "message": "update schedule success."
        })

    @record_operation_log
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "code": 20000,
            "message": "delete schedule success."
        })


class PeriodicTaskViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions, )

    queryset = PeriodicTask.objects.all().order_by("-id")
    serializer_class = PeriodicTaskSerializer

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
            "message": "create task success."
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
            "message": "update task success."
        })

    @record_operation_log
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "code": 20000,
            "message": "delete task success."
        })


class TaskResultViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions, )

    queryset = TaskResult.objects.all().order_by("-id")
    serializer_class = TaskResultSerializer

    def _is_reload_queryset(self):
        return TaskResult.objects.count() != len(self.queryset)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against query parameter in the URL.
        """
        queryset = TaskResult.objects.all().order_by("-id")

        # 检测后端数据是否变化, 判断缓存是否需要重载, 需要优化当条目更新时也能检测到数据变化
        # if self._is_reload_queryset():
        #     queryset = TaskResult.objects.all().order_by("-id")

        _filter_kwargs = {}
        task_id = self.request.query_params.get('task_id', None)
        time_range = self.request.query_params.getlist('time_range[]', None)
        task_name = self.request.query_params.get('name', None)
        if task_id:
            _filter_kwargs['task_id'] = task_id

        if task_name:
            _filter_kwargs['task_name'] = task_name

        if time_range:
            _filter_kwargs['date_created__gte'] = time_range[0]
            _filter_kwargs['date_created__lte'] = time_range[-1]

        if _filter_kwargs:
            queryset = queryset.filter(**_filter_kwargs).order_by("-id")

        return queryset

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
