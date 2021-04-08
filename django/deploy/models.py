from django.db import models
from django.contrib.auth.models import User
from k8s.models import KubernetesCluster
# Create your models here.


class Service(models.Model):

    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=150, blank=True)
    repo = models.CharField(max_length=50)
    chart_dir = models.CharField(max_length=50)
    create_time = models.DateTimeField(
        blank=True, null=True, auto_now_add=True, auto_now=False)
    update_time = models.DateTimeField(blank=True, null=True, auto_now=True)
    enabled = models.BooleanField(default=True, null=True, blank=True)


class Release(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.CharField(max_length=50, blank=True)
    task_id = models.CharField(max_length=50, blank=True)
    log = models.CharField(max_length=50, blank=True)
    value_file = models.CharField(max_length=50, blank=True)
    cluster = models.ForeignKey(
        KubernetesCluster, on_delete=models.CASCADE)
    namespace = models.CharField(max_length=50, blank=True)
    args = models.CharField(max_length=150, blank=True)
    create_time = models.DateTimeField(
        blank=True, null=True, auto_now_add=True, auto_now=False)
    update_time = models.DateTimeField(blank=True, null=True, auto_now=True)
    description = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=50, blank=True)
    revision = models.IntegerField(default=0)
