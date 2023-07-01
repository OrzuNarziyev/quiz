import redis, json
from django.conf import settings
from datetime import datetime

r = redis.Redis(
    host=settings.REDIS_HOST,
    db=settings.REDIS_DB,
    port=settings.REDIS_PORT
)


class RecentActivity:
    def __init__(self, user):
        self.__user = user

    def data_res(self, data):
        data = json.loads(data)
        date_act = datetime.fromtimestamp(data.get('date'))
        data['date'] = date_act

        return data

    def __iter__(self):
        dates = r.lrange(self.get_resent_key(), 0, 7)
        for data in dates:
            yield self.data_res(data)

    def get_resent_key(self):
        return f"resent:{self.__user}-user"

    def add_resent_activity(self, data: dict):
        list_act = r.lrange(self.get_resent_key(), 0, -1)
        for x in list_act:
            data_r = json.loads(x)
            if data['category'] == data_r['category'] and data['title'] == data_r['title']:
                r.lrem(self.get_resent_key(), 1, x)

        r.lpush(self.get_resent_key(), json.dumps(data))

    # def get_resent_activity(self):
    #
    #     list_activity = r.lrange(self.get_resent_key(), 0, -1)
    #
    #     return [json.loads(x) for x in list_activity]
