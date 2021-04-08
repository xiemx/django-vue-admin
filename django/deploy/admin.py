from django.contrib import admin

# Register your models here.
from deploy.models import Service, Release

admin.site.register(Service)
admin.site.register(Release)
