

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomUser, UserProfile


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email','first_name','last_name')}),
    )



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)