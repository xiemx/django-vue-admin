from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class UserGuardianAdmin(GuardedModelAdmin, UserAdmin):
    pass


admin.site.unregister(User)
admin.site.register(User, UserGuardianAdmin)
