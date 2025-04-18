

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomUser, UserProfile


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email','first_name','last_name')}),
    )

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = CustomUser.objects.get(pk=obj.pk)
            if obj.password != old_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)