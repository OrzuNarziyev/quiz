import json
from datetime import datetime

from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse

from account.utils import auth_token
from account.utils.auth_token import get_info
from account.data_user import UserDataMixin
from account.models import CustomUser, Organizations
# import redis
from django.conf import settings
from account.translate import to_latin, to_cyrillic
from account.translate import to_latin, to_cyrillic
import redis, json

r = redis.Redis(
    host=settings.REDIS_HOST,
    db=settings.REDIS_DB,
    port=settings.REDIS_PORT
)


def account_info(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        pinfl = request.user.pinfl
        try:
            user = json.loads(r.get(pinfl))
        except:
            user = None
        if user:
            context = {
                'organization': user['organization']['railway'] if str(user['organization']['railway']).isascii() else
                user['organization']['railway'],

                'fullname': to_cyrillic(user['fullname']) if str(user['fullname']).isascii() else user['fullname'],

                'staff_full': to_cyrillic(user['staff'][0]['staff_full']) if str(
                    user['staff'][0]['staff_full']).isascii() else user['staff'][0]['staff_full'],

                'department': to_cyrillic(user['staff'][0]['department_id']['name']) if str(
                    user['staff'][0]['department_id']['name']).isascii() else user['staff'][0]['department_id']['name'],

                'organisation_name': to_cyrillic(user['organization']['name']) if str(
                    user['organization']['name']).isascii() else \
                    user['organization']['name'],

                'photo': user['photo']
            }
            return context
        else:
            print('hello world info')
            status = auth_token.get_info(request.user.pinfl)
            if status == 200:
                user = cache.get(pinfl)
                print(user)
                context = {
                    'organization': user['organization']['railway'],
                    'fullname': to_cyrillic(user['fullname']),
                    'photo': user['photo'],
                    'staff_full': user['staff'][0]['staff_full'],
                    'department': user['staff'],
                    'organisation_name': user['organization']['name']
                }
                return context
            else:
                return {}

    return {}
