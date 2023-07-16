from django.db import models
import os
import random
from io import BytesIO

import uuid as uuid
from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File as F
from PIL import ImageDraw, Image as Img
from django.urls import reverse

from quiz.fields import OrderField
from account.models import CustomUser
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Category(MPTTModel):
    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required and unique"),
        max_length=255,
    )
    slug = models.SlugField(verbose_name=_(
        "Category safe URL"), max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE,
                            null=True, blank=True, related_name="children")
    is_active = models.BooleanField(default=True)
    icon = models.ImageField()

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def icon_url(self):
        return self.icon

    def __str__(self):
        return self.name


class Quiz(models.Model):
    yakuniy = 'yk'
    sinov_test = 'st'
    title_choices = [
        (yakuniy, 'Yakuniy nazorat'),
        (sinov_test, 'Sinov test'),
    ]

    category = TreeForeignKey("quiz.Category", on_delete=models.CASCADE, null=True, blank=True,
                              related_name='quizs',
                              verbose_name='Bo\'lim', help_text="Bo'limni tanlang")
    course = models.ForeignKey(
        "course.Course", on_delete=models.CASCADE, related_name='quizs_course', blank=True, null=True)
    module = models.ForeignKey("course.Module", verbose_name=_(
        "module"), on_delete=models.CASCADE, blank=True, null=True, related_name='quizs_module')

    title = models.CharField(verbose_name='Sarlavha', choices=title_choices, default=yakuniy,
                             max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    number_of_questions = models.IntegerField(
        verbose_name="Test savollari soni", blank=True)
    score_to_pass = models.IntegerField(
        verbose_name='o\'tish bali', help_text="O'tish uchun eng past ball (1 ~ 100 oralig'ida)")
    time = models.IntegerField(
        verbose_name='test vaqti', help_text="test yechish uchun vaqt davomiyligi")
    created = models.DateTimeField(auto_now_add=True)
    period_date = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=False)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    #
    def __str__(self):
        return f"{self.category}"

    def get_questions(self):
        questions = list(self.questions.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]

    # def save(self, *args, **kwargs):
    #     qrcode_img = qrcode.make(f"")
    #     canvas = Img.new('RGB', (450, 450), 'white')
    #     draw = ImageDraw.Draw(canvas)
    #     canvas.paste(qrcode_img)
    #     fname = f"{str(self.course).strip(' ')}" + '.png'
    #     buffer = BytesIO()
    #     canvas.save(buffer, 'PNG')
    #     self.qr_photo.save(fname, F(buffer), save=False)
    #     canvas.close()
    #     super().save(*args, **kwargs)

    class Meta:
        ordering = ['category', 'course', 'module']


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='questions')
    # text=CKEditor5Field('Text', config_name='extends')
    # text = RichTextUploadingField()
    text = models.TextField(blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4(), editable=False, unique=True)

    created = models.DateTimeField(auto_now_add=True)
    order = OrderField(blank=True, for_fields=['quiz'], null=True)

    # def __str__(self):
    #     return f"{self.text}"

    def get_answers(self):
        answers = list(self.answers.all())
        random.shuffle(answers)
        return answers

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['created']


class Answer(models.Model):
    # text=CKEditor5Field('Text', config_name='extends')
    # text = RichTextUploadingField()
    text = models.TextField(blank=True, null=True)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers')
    created = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    order = OrderField(blank=True, for_fields=['question'], null=True)

    def __str__(self):
        return f'savol: {self.question.text} - javob: {self.correct}'

    class Meta:
        ordering = ['-created']


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE,
                             related_name='result', related_query_name='result')
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='result')
    score = models.FloatField()
    attempts = models.IntegerField(
        verbose_name='urinishlar soni', help_text='Urinishlar soni', default=1)
    date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}: result {self.score}"

    def result(self):
        return f"{self.user}: result {self.score}"


# class Sertificate(models.Model):
#     def content_image_name(instance, filename):
#         return '/'.join([f'{instance.course}', str(instance.student), filename])

#     uuid = models.UUIDField(default=uuid.uuid4, editable=False)
#     # course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sertificate')
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sertificate',
#                                 related_query_name='sertificate')
#     qr_photo = models.ImageField(editable=False, upload_to=content_image_name, blank=True)
#     created = models.DateField(auto_now_add=True)

#     def get_absolute_url(self):
#         return reverse('account:sertificate', kwargs={'uuid': self.uuid})

#     def save(self, *args, **kwargs):
#         try:
#             if len(self.qr_photo) > 0:
#                 os.remove(self.qr_photo.path)
#         except:
#             pass

#         qrcode_img = qrcode.make(f"{self.get_absolute_url()}")
#         canvas = Img.new('RGB', (450, 450), 'white')
#         draw = ImageDraw.Draw(canvas)
#         canvas.paste(qrcode_img)
#         fname = f"{str(self.student).strip(' ')}" + '.png'
#         buffer = BytesIO()
#         canvas.save(buffer, 'PNG')
#         self.qr_photo.save(fname, F(buffer), save=False)
#         canvas.close()
#         super().save(*args, **kwargs)

class ExcelFileUploaded(models.Model):
    excel_file = models.FileField(upload_to='excel', verbose_name='Excel File')
