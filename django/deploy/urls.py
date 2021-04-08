from django.conf.urls import url, include
from rest_framework import routers

from deploy.views import ServiceViewSet, ReleaseViewSet


router = routers.DefaultRouter()
router.register(r'service', ServiceViewSet)
router.register(r'release', ReleaseViewSet)


urlpatterns = [
    url('', include(router.urls)),
]
