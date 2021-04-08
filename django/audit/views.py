from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoModelPermissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from audit.models import UserOperationLog
from audit.serializers import UserOperationLogSerializer
from common.audit_decorator import record_operation_log


class UserOperationLogViewSet(viewsets.ModelViewSet):

    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = UserOperationLog.objects.all().order_by("-id")
    serializer_class = UserOperationLogSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against query parameter in the URL.
        """
        queryset = UserOperationLog.objects.all().order_by("-id")

        _filter_kwargs = {}

        cluster = self.request.query_params.get('cluster', None)
        username = self.request.query_params.get('username', None)
        resource = self.request.query_params.get('resource', None)
        operation = self.request.query_params.get('operation', None)
        time_range = self.request.query_params.getlist('time_range[]', None)

        if username:
            _filter_kwargs['user__username'] = username

        if resource:
            _filter_kwargs['resource'] = resource

        if operation:
            _filter_kwargs['operation'] = operation

        if time_range:
            _filter_kwargs['create_time__gte'] = time_range[0]
            _filter_kwargs['create_time__lte'] = time_range[-1]

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

        _content = {
            "code": 20000,
            "data": {
                "total": len(queryset),
                "items": serializer.data
            }
        }

        return Response(_content)
