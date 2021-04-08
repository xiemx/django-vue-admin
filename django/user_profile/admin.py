from django.contrib import admin
from user_profile.models import profile

from guardian.admin import GuardedModelAdmin


class ProfileAdmin(GuardedModelAdmin):
    pass


admin.site.register(profile, ProfileAdmin)
