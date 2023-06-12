from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from account.models import CustomUser


@receiver(post_save, sender=CustomUser)
def user_info_signal(sender, **kwargs):
    pass
