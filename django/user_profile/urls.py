from django.conf.urls import url, include
from rest_framework import routers

from user_profile.views import (
    UserProfileViewSet,

)

router = routers.DefaultRouter()
router.register(r'', UserProfileViewSet)


urlpatterns = [
    url('', include(router.urls)),
]
