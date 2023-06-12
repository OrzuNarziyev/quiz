from django.conf import settings
from django.core.cache import cache
from account.utils import auth_token
import redis
import json

r = redis.Redis(
    host=settings.REDIS_HOST,
    db=settings.REDIS_DB,
    port=settings.REDIS_PORT
)


# class UserData:
#
#     def __init__(self, request):
#         self.session = request.session
#         user = self.session.get(settings.USER_SESSION_ID)
#
#         if request.user.is_authenticated and not request.user.is_superuser:
#             print('hello is admin nnot')
#             if not user:
#                 context = auth_token.get_info(request.user.pinfl)
#                 if context is not None:
#                     user = self.session[settings.USER_SESSION_ID] = context['cadry']
#                     # user.set_expire(120)
#
#             self.user = user
#
#         #
#         # if request.user.is_authenticated:
#         #     if not request.user.is_superuser:
#         #         if not user:
#         #             print('not user')
#         #             context = auth_token.get_info(request.user.pinfl)
#         #             if context is not None:
#         #
#         #                 user = self.session[settings.USER_SESSION_ID] = context['cadry']
#         #                 self.session.set_expiry(120)
#
#     def add(self, data):
#         self.user['data'] = data
#
#     def get_info(self):
#         return self.user
#
#     def save(self):
#         self.session.modified = True
#
#     def clear(self):
#         del self.session[settings.USER_SESSION_ID]
#         self.save()

class UserDataMixin:

    def __init__(self, request):
        self.pinfl = request.user.pinfl

        user = cache.get(self.pinfl)
        print(user, 'data user')

        if not user:
            print('user qidirishga kirdi')
            context = auth_token.get_info(self.pinfl)
            print(type(context))
            if context is not None:
                cache.set(self.pinfl, context)
                user = cache.get(self.pinfl)
        self.user = user

        # user = self.session.get(settings.USER_SESSION_ID)
        #
        # if request.user.is_authenticated:
        #     if not request.user.is_superuser:
        #         if not user:
        #             print('not user')
        #             context = auth_token.get_info(request.user.pinfl)
        #             if context is not None:
        #
        #                 user = self.session[settings.USER_SESSION_ID] = context['cadry']
        #                 self.session.set_expiry(120)

    # def add(self, data):
    #     self.user['data'] = data
    #
    # def get_info(self):
    #     return self.user
    #
    # def save(self):
    #     self.session.modified = True
    #
    # def clear(self):
    #     del self.session[settings.USER_SESSION_ID]
    #     self.save()
