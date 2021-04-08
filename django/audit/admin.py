from django.contrib import admin
from audit.models import UserOperationLog

# Register your models here.
admin.site.register(UserOperationLog)
