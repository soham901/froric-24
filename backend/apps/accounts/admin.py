from django.contrib import admin

from .models import CustomUser, BasicRoleDemo


admin.site.register(CustomUser)

admin.site.register(BasicRoleDemo)
