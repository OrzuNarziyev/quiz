from django.contrib import admin
from .models import Course, Module, Content, Image, Text, Video
from quiz.models import Category
from mptt.admin import TreeRelatedFieldListFilter, MPTTModelAdmin


# Register your models here.

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'parent']


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject']
    list_filter = ['created', 'subject']
    prepopulated_fields = {'slug': ('title', 'subject')}
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
    list_display = ['order', 'title']
    list_filter = (
        'course',
    )


@admin.register(Text)
class CourseText(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id']
    # list_filter = ['created', 'subject']
    # prepopulated_fields = {'slug': ('title', 'subject')}
    # inlines = [ModuleInline]


admin.site.register(Content)
admin.site.register(Image)
# admin.site.register(Text)
admin.site.register(Video)
