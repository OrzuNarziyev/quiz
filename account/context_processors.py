import json
from datetime import datetime

from django.core.cache import cache

from account.utils import auth_token
from account.utils.auth_token import get_info
from account.data_user import UserDataMixin
from account.models import CustomUser, Organizations
# import redis
from django.conf import settings
from account.translate import to_latin, to_cyrillic
from account.translate import to_latin, to_cyrillic

# r = redis.Redis(
#     host=settings.REDIS_HOST,
#     db=settings.REDIS_DB,
#     port=settings.REDIS_PORT
# )


def account_info(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        pinfl = request.user.pinfl
        user = cache.get(pinfl)

        if user:
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
            status = auth_token.get_info(request.user.pinfl)
            if status == 200:
                user = cache.get(pinfl)
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
