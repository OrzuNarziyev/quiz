import redis, json
from django.conf import settings

r = redis.Redis(
    host=settings.REDIS_HOST,
    db=settings.REDIS_DB,
    port=settings.REDIS_PORT
)
class RecentActivity:
    def get_resent_key(self, user):
        return f"resent:{user}-user"

    def add_resent_activity(self, data):
        pass
