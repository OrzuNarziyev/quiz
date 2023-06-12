from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin, TreeRelatedFieldListFilter

from .models import CustomUser, Organizations, Staff_user

# Register your models here.
# admin.site.register(CustomUser)
# admin.site.register(Organizations)
admin.site.register(Staff_user)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['pinfl', 'username']


@admin.register(Organizations)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 50
    list_filter = (
        ('parent', TreeRelatedFieldListFilter),
    )
