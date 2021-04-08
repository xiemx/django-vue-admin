from django.contrib import admin
from toolkit.models import toolKitExam, toolKitIngressWhitelist, toolKitKubernetesCleaner, toolKitGraphiteCleaner, toolKitAutoScaling

# Register your models here.

admin.site.register(toolKitExam)
admin.site.register(toolKitIngressWhitelist)
admin.site.register(toolKitKubernetesCleaner)
admin.site.register(toolKitAutoScaling)
admin.site.register(toolKitGraphiteCleaner)
