from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from account.views import GitlabOAuth2Callback, UserViewSet, GroupViewSet, TokenJWTViewSet, PermsViewSet, KubernetesRBACviewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'group', GroupViewSet)
router.register(r'permission', PermsViewSet)
router.register(r'rbac-k8s', KubernetesRBACviewSet)


urlpatterns = [
    path("user/login/", TokenJWTViewSet.as_view()),

    url('', include(router.urls)),
    path('admin/', admin.site.urls),
    url(r'toolkit/', include('toolkit.urls')),
    url(r'deploy/', include('deploy.urls')),
    url(r'k8s/', include('k8s.urls')),
    url(r'audit/', include('audit.urls')),
    url(r'job/', include('job.urls')),
    # url(r'profile/', include('user_profile.urls')),

    path('accounts/login/callback/', GitlabOAuth2Callback),
    url(r'^accounts/login/', include('django_gitlab_auth.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
