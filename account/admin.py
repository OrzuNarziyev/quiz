from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin, TreeRelatedFieldListFilter

from .models import CustomUser, Organizations, Staff_user
from django.contrib.auth.admin import UserAdmin

from django.utils.translation import gettext_lazy as _

# Register your models here.
# admin.site.register(CustomUser)
# admin.site.register(Organizations)
admin.site.register(Staff_user)


# admin.site.register(Group)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['pinfl', 'username']
    ordering = ('-date_joined',)
    list_filter = (("organizations", TreeRelatedFieldListFilter), "is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("pinfl", "username", "first_name", "last_name", "email")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("pinfl", "first_name", "last_name", "email")}),
        (_("Organizations info"), {"fields": ("organizations", "staff_user")}),
        (
            _("Permissions"),
            {
                "fields": (

                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


@admin.register(Organizations)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 50
    list_filter = (
        ('parent', TreeRelatedFieldListFilter),
    )
