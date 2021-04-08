from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, DjangoObjectPermissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from common.audit_decorator import record_operation_log
from rest_framework import viewsets

from user_profile.models import profile
from user_profile.serializers import UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    user profile
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (
        IsAuthenticated, DjangoModelPermissions)
    queryset = profile.objects.all()
    serializer_class = UserProfileSerializer

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

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        return Response({
            "code": 20000,
            "message": "稍后查看任务状态，清理 Graphite disk 任务进行中..."
        })

    @record_operation_log
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            "code": 20000,
            "data": "更新 Group 成功。"
        })
