from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class profile(models.Model):
    """
    autoscaling
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    avatar = models.CharField(max_length=150, blank=True, null=True)
    alicloud = models.CharField(max_length=50, blank=True, null=True)
    dingding = models.CharField(
        max_length=50, blank=True, null=True)  # 不支持用户自行变更
    phone = models.CharField(max_length=20, blank=True, null=True)
    update_time = models.DateTimeField(
        blank=True, null=True, auto_now=True)

    class Meta:
        db_table = "user_profile"
