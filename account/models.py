from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, User
from django.db import models

from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _


# FIO, ish joyi, lavozimi, telfon raqam, login, parol


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, blank=True, null=True, unique=True)
    #
    # phone_number = models.CharField(_('phone_number'), unique=True, max_length=20)
    # profile_image = models.ImageField(upload_to='user/images/', blank=True)
    # # father name
    # father_name = models.CharField(_('father_name'), max_length=100, blank=True, null=True)
    # last_name = models.CharField(_('last_name'), max_length=100, blank=True, null=True)
    # first_name = models.CharField(_('first_name'), max_length=100, blank=True, null=True)
    # work_place = models.ForeignKey('Work_place', on_delete=models.CASCADE, null=True, blank=True)
    # position = models.ForeignKey('Grade', on_delete=models.CASCADE, null=True, blank=True)
    pinfl = models.CharField(max_length=50, verbose_name='JSHSHR', unique=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['pinfl']

    # objects = CustomUserManager()

    # def get_full_name(self):
    #     return f"{self.last_name} {self.first_name}  {self.father_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Organizations(MPTTModel):
    organization = models.CharField(max_length=255, verbose_name=_('Organization'), blank=True, null=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE,
                            null=True, blank=True, related_name="children")

    def __str__(self):
        return self.organization


class Staff_user(models.Model):
    staff = models.CharField(max_length=255, verbose_name='lavozim')

    def __str__(self):
        return self.staff
