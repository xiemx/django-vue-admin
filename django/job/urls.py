from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path


from job.views import (
    IntervalScheduleViewSet,
    ClockedScheduleViewSet,
    CrontabScheduleViewSet,
    PeriodicTaskViewSet,
    SolarScheduleViewSet,
    TaskResultViewSet
)

from common.auxiliary_func import fetch_celery_registered_tasks


router = routers.DefaultRouter()
router.register(r'interval', IntervalScheduleViewSet)
router.register(r'clocked', ClockedScheduleViewSet)
router.register(r'crontab', CrontabScheduleViewSet)
router.register(r'solar', SolarScheduleViewSet)
router.register(r'task', PeriodicTaskViewSet)
router.register(r'task_result', TaskResultViewSet)
urlpatterns = [
    url('', include(router.urls)),
    url(r'celery-registered-tasks', fetch_celery_registered_tasks)
]
