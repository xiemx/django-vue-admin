from django.conf.urls import url, include
from rest_framework import routers

from audit.views import UserOperationLogViewSet

router = routers.DefaultRouter()
router.register(r'operation', UserOperationLogViewSet)


urlpatterns = [
    url('', include(router.urls)),
]
