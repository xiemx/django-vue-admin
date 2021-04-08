from django_gitlab_auth import oidc
from django.contrib.auth.models import User, Group, Permission
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, PermsSerializer
from django.shortcuts import HttpResponse, redirect
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoModelPermissions, DjangoObjectPermissions
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.utils import jwt_response_payload_handler, jwt_decode_handler
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from django.urls import reverse
from .utils import get_user_info_for_gitlab
import json
from user_profile.models import profile
from k8s.models import KubernetesDeployment, KubernetesCluster
from k8s.serializers import KubernetesDeploymentSerializer

from rest_framework_jwt.settings import api_settings
from common.audit_decorator import record_operation_log
from django.conf import settings


class UserViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (
        IsAuthenticated, DjangoModelPermissions, DjangoObjectPermissions)

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    # 列出所有用户
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

    # 获取用户信息
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            "code": 20000,
            "data":  serializer.data
        })

    # 更新用户信息
    @record_operation_log
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        _data = request.data

        # 无法嵌套更新 profile, 单独处理
        _profile = _data.get("profile", None)
        if _profile:
            instance.profile = profile(**_profile)
            instance.profile.save()

        # 不支持创建嵌套用户，删除 one_to_one 信息单独处理
        if "profile" in _data.keys():
            del _data['profile']

        serializer = self.get_serializer(
            instance, data=_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response({
            "code": 20000,
            "message":  "更新用户信息成功。"
        })


class GroupViewSet(viewsets.ModelViewSet):
    """
    允许组查看或编辑的API路径。
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

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
        self.perform_create(serializer)
        users = [User.objects.get(username=i) for i in request.data['users']]
        Group.objects.get(name=request.data['name']).user_set.set(users)
        return Response({
            "code": 20000,
            "message": "创建 Group 成功。"
        })

    @record_operation_log
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # 更新用户权限组（so bad 如何直接在序列化过程中save？）
        users = [User.objects.get(username=i) for i in request.data['users']]
        instance.user_set.set(users)

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
            "data": "更新成功。"
        })

    @record_operation_log
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "code": 20000,
            "message": "删除 Group 成功."
        })


class PermsViewSet(viewsets.ModelViewSet):
    """
    允许组查看或编辑的API路径。
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    queryset = Permission.objects.all()
    serializer_class = PermsSerializer

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


class KubernetesRBACviewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = KubernetesDeployment.objects.all()
    serializer_class = KubernetesDeploymentSerializer

    def __get_queryset(self, client):
        cluster_role_list = client.list_cluster_role_binding().items
        role_list = client.list_role_binding_for_all_namespaces().items
        queryset = []

        for user in User.objects.all():
            namespace = []
            cluster_role = []
            try:
                for rb in role_list:
                    if rb.subjects:
                        for subject in rb.subjects:
                            if subject.kind == "User" and subject.name == user.profile.alicloud:
                                namespace.append(rb.metadata.namespace)
                            # print("%s\t%s\t%s" %
                            #       (subject.name, rb.role_ref.name, rb.metadata.namespace))

                for crb in cluster_role_list:
                    if crb.subjects:
                        for subject in crb.subjects:
                            if subject.kind == "User" and subject.name == user.profile.alicloud:
                                cluster_role.append(crb.role_ref.name)
            except Exception as err:
                print(err)

            finally:
                queryset.append({
                    "username": user.username,
                    "cluster_role": cluster_role,
                    "namespace": namespace
                })

        return queryset

    def list(self, request, *args, **kwargs):
        cluster_name = request.query_params["cluster"]
        cluster = KubernetesCluster.objects.get(
            name=cluster_name)
        client = KubernetesDeployment.get_client(cluster_config=cluster.config)
        v1 = client.RbacAuthorizationV1Api()
        queryset = self.__get_queryset(client=v1)

        return Response({
            "code": 20000,
            "data": {
                "total": len(queryset),
                "items": queryset
            }
        })


class TokenJWTViewSet(ObtainJSONWebToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            token_data = jwt_response_payload_handler(token, user, request)
            response_data = {
                'code': 20000,
                'data': token_data
            }
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=False)
            return response

        return Response({
            "code": 50001,
            "message": "User or Password is invaild."
        })


def GitlabOAuth2Callback(request):

    res = oidc.server.request_token(
        redirect_uri=request.build_absolute_uri(
            reverse("django_gitlab_auth:callback")),
        code=request.GET["code"],
    )
    user_info = get_user_info_for_gitlab(res.id["sub"], res.access_token)

    email = user_info.get(
        'email', "{}@{}".format(user_info.get("username"), settings.EMAIL_SUFFIX))

    user, created = User.objects.get_or_create(
        username=res.id["sub"], email=email)

    # 首次登陆时获取 avatar 信息
    if created:
        user.profile = profile(avatar=user_info.get("avatar_url", None))
        user.profile.save()

    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    response_data = {
        'code': 20000,
        'data': {
            'token': token
        }
    }

    response = redirect(settings.GITLAB_OAUTH_REDIRECT)

    if api_settings.JWT_AUTH_COOKIE:
        expiration = (datetime.utcnow() +
                      api_settings.JWT_EXPIRATION_DELTA)
        response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                            token,
                            expires=expiration,
                            httponly=False,
                            samesite='lax'
                            )
    return response
