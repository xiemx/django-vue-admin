from rest_framework import serializers
from django_celery_beat.models import (
    IntervalSchedule,
    SolarSchedule,
    CrontabSchedule,
    ClockedSchedule,
    PeriodicTask
)

from django_celery_results.models import TaskResult


class IntervalScheduleSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = IntervalSchedule
        fields = "__all__"
        ordering = ('-id')


class SolarScheduleSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = SolarSchedule
        fields = "__all__"
        ordering = ('-id')


class CrontabScheduleSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    # timezone = serializers.StringRelatedField()
    # 增加自定义属性

    def to_representation(self, value):
        data = super().to_representation(value)
        data['timezone'] = value.timezone.__str__()

        return data

    class Meta:
        model = CrontabSchedule
        fields = "__all__"


class ClockedScheduleSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ClockedSchedule
        fields = "__all__"


class PeriodicTaskSerializer(serializers.HyperlinkedModelSerializer):

    interval = serializers.PrimaryKeyRelatedField(
        queryset=IntervalSchedule.objects.all(), many=False, allow_null=True, default=None)
    crontab = serializers.PrimaryKeyRelatedField(
        many=False, queryset=CrontabSchedule.objects.all(),  allow_null=True, default=None)
    clocked = serializers.PrimaryKeyRelatedField(
        many=False, queryset=ClockedSchedule.objects.all(),  allow_null=True, default=None)
    solar = serializers.PrimaryKeyRelatedField(
        many=False, queryset=SolarSchedule.objects.all(), allow_null=True, default=None)

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PeriodicTask
        fields = "__all__"
        ordering = ('-id')


class TaskResultSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = TaskResult
        fields = "__all__"
        ordering = ('-id')
