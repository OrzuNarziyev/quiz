from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from quiz.models import Result
from django.conf import settings
import redis, json

r = redis.Redis(
    host=settings.REDIS_HOST,
    db=settings.REDIS_DB,
    port=settings.REDIS_PORT
)


@receiver(post_save, sender=Result)
def add_statistics_save(sender, instance, **kwargs):
    user = instance.user
    results = Result.objects.filter(user=user, quiz__module__isnull=True).order_by('date').values('pk', 'score', 'date')
    data = dict()
    for x in results:
        day = x.get('date').strftime('%x')
        a = data.get(day)
        if a:
            data[day].append(x)
        else:
            data[day] = [x]
    labels = []
    data_chartjs = []
    for x in data:
        score = 0
        for y in data[x]:
            score += y['score']
        labels.append(x)
        data_chartjs.append(score / len(data[x]))
    if r.get(f"user:{user}:result"):
        r.delete(f"user:{user}:result")
    r.set(f"user:{user}:result", json.dumps({
        'labels': labels,
        'data': data_chartjs
    }))

@receiver(post_delete, sender=Result)
def add_statistics_delete(sender, instance, **kwargs):
    user = instance.user
    results = Result.objects.filter(user=user, quiz__module__isnull=True).order_by('date').values('pk', 'score', 'date')
    data = dict()
    for x in results:
        day = x.get('date').strftime('%x')
        a = data.get(day)
        if a:
            data[day].append(x)
        else:
            data[day] = [x]
    labels = []
    data_chartjs = []
    for x in data:
        score = 0
        for y in data[x]:
            score += y['score']
        labels.append(x)
        data_chartjs.append(score / len(data[x]))
    if r.get(f"user:{user}:result"):
        r.delete(f"user:{user}:result")
    r.set(f"user:{user}:result", json.dumps({
        'labels': labels,
        'data': data_chartjs
    }))
