from django.db import models
from quiz.models import Category
from mptt.models import TreeForeignKey, MPTTModel
from django.template.loader import render_to_string

# Create your models here.

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from quiz.fields import OrderField


class Course(models.Model):
    subject = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True)

    def __str__(self) -> str:
        return f"{self.title}"


class Module(MPTTModel):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    # description = models.TextField(blank=True)
    parent = TreeForeignKey('self', verbose_name="Bo'lim", on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    order = OrderField(blank=True, for_fields=['course'])

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        ordering = ['order']


class Content(models.Model):
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name='contents'
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'text',
                                         'video',
                                         'image',
                                         'file')})

    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])


class ItemBase(models.Model):
    title = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string(
            f'course/dashboard/manage/content/{self._meta.model_name}.html', {'item': self})


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    url = models.URLField()
