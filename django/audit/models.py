from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField
# Create your models here.


class UserOperationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.CharField(max_length=50)
    operation = models.CharField(max_length=50)
    before = JSONField(help_text="json format.",
                       null=True,
                       )
    content = JSONField(help_text="json format.",
                        null=True,
                        )
    create_time = models.DateTimeField(auto_now=True)
