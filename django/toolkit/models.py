from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import User
from k8s.models import KubernetesCluster
# Create your models here.


class toolKitExam(models.Model):
    """
    exam
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.CharField(max_length=50, blank=True, null=True)
    create_time = models.DateTimeField(
        blank=True, null=True, auto_now_add=True, auto_now=False)
    update_time = models.DateTimeField(blank=True, null=True, auto_now=True)
    exam_id = models.CharField(max_length=50, blank=True, null=True)
    exam_url = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)


class toolKitIngressWhitelist(models.Model):
    """
    ingress whitelist
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.CharField(max_length=50, blank=True, null=True)
    create_time = models.DateTimeField(
        blank=True, null=True, auto_now_add=True, auto_now=False)
    update_time = models.DateTimeField(blank=True, null=True, auto_now=True)
    status = models.CharField(max_length=50, blank=True, null=True)


class toolKitKubernetesCleaner(models.Model):
    """
    k8s resource cleaner
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.CharField(max_length=50, blank=True, null=True)
    cluster = models.ForeignKey(
        KubernetesCluster, on_delete=models.CASCADE, null=True)
    pods = ArrayField(models.CharField(
        max_length=200, blank=True), default=list)
    create_time = models.DateTimeField(
        blank=True, null=True, auto_now_add=True, auto_now=False)
    update_time = models.DateTimeField(
        blank=True, null=True, auto_now=True)
    status = models.CharField(max_length=50, blank=True, null=True)


class toolKitAutoScaling(models.Model):
    """
    autoscaling
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.CharField(max_length=50, blank=True, null=True)
    namespace = models.CharField(max_length=50, blank=True, null=True)
    service = models.CharField(max_length=50, blank=True, null=True)
    number = models.IntegerField()
    product = models.CharField(max_length=50, blank=True, null=True)
    create_time = models.DateTimeField(
        blank=True, null=True, auto_now_add=True, auto_now=False)
    update_time = models.DateTimeField(
        blank=True, null=True, auto_now=True)
    status = models.CharField(max_length=50, blank=True, null=True)


class toolKitGraphiteCleaner(models.Model):
    """
    graphite cleaner
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.CharField(max_length=50, blank=True, null=True)
    create_time = models.DateTimeField(
        blank=True, null=True, auto_now_add=True, auto_now=False)
    update_time = models.DateTimeField(blank=True, null=True, auto_now=True)
    status = models.CharField(max_length=50, blank=True, null=True)
