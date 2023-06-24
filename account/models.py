from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, User, UserManager, PermissionsMixin
from django.db import models

from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _


# FIO, ish joyi, lavozimi, telfon raqam, login, parol


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, blank=True, null=True, unique=True)
    organizations = models.ForeignKey('Organizations', on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='users')
    staff_user = models.ForeignKey('Staff_user', on_delete=models.CASCADE, related_name='user', null=True)
    pinfl = models.CharField(max_length=50, verbose_name='JSHSHR', unique=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['pinfl']

    # objects = UserManager()

    # objects = CustomUserManager()

    # def get_full_name(self):
    #     return f"{self.last_name} {self.first_name}  {self.father_name}"

    # def __str__(self):
    #     return f"{self.first_name} {self.last_name}"
    def __str__(self):
        return f"{self.pinfl} {self.last_name}"


class Organizations(MPTTModel):
    organization = models.CharField(max_length=255, verbose_name=_('Organization'), blank=True, null=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE,
                            null=True, blank=True, related_name="children")

    def __str__(self):
        return self.organization


class Staff_user(models.Model):
    organization = models.ForeignKey(Organizations, on_delete=models.CASCADE, related_name='staff_user', null=True)
    staff = models.CharField(max_length=255, verbose_name='lavozim')

    def __str__(self):
        return self.staff
