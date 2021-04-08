from django.conf.urls import url, include
from rest_framework import routers

from toolkit.views import (
    ToolKitExamViewSet,
    ToolKitIngressWhitelistViewSet,
    ToolKitKubernetesCleanerViewSet,
    ToolKitGraphiteCleanerViewSet,
    ToolKitAutoScalingViewSet
)

router = routers.DefaultRouter()
router.register(r'exam', ToolKitExamViewSet)
router.register(r'ingress-whitelist', ToolKitIngressWhitelistViewSet)
router.register(r'k8s-cleaner', ToolKitKubernetesCleanerViewSet)
router.register(r'autoscaling', ToolKitAutoScalingViewSet)
router.register(r'graphite-cleaner', ToolKitGraphiteCleanerViewSet)

urlpatterns = [
    url('', include(router.urls)),
]
