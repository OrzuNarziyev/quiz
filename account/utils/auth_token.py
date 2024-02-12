import io

import requests
from django.core.cache import cache
from account.data_user import UserDataMixin
from django.conf import settings
import base64
from datetime import datetime

import redis, json

r = redis.Redis(
    host=settings.REDIS_HOST,
    db=settings.REDIS_DB,
    port=settings.REDIS_PORT
)

email = 'railtest-coll@railway.ajk'
password = 'RailWayTest12345%^&'
login_endpoint = 'https://api-exodim.railway.uz/api/auth/collaborator/login'
endpoint = "https://api-exodim.railway.uz/api/collaborator/cadry/check"


def get_info(pinfl):
    if cache.get('access_token') is None:
        print('not access')
        api_login()
        token = cache.get('access_token')
        type_api = cache.get('token_type')
        if isinstance(token, bytes):
            headers = {
                'Authorization': f"{type_api.decode()} {token.decode()}"
            }
        else:
            headers = {
                'Authorization': f"{type_api} {token}"
            }

    else:
        print('has access token')
        token = cache.get('access_token')
        type_api = cache.get('token_type')
        print(token)

        if isinstance(token, bytes):
            headers = {
                'Authorization': f"{type_api.decode()} {token.decode()}"
            }
        else:
            headers = {
                'Authorization': f"{type_api} {token}"
            }
    get_response = requests.get(endpoint, headers=headers, params={"pinfl": pinfl})
    print(get_response)
    if get_response.status_code == 200:
        data = get_response.json()['cadry']
        data['date'] = datetime.now().timestamp()
        r.set(pinfl, json.dumps(data))

        return get_response.status_code

    elif get_response.status_code == 404:
        return get_response.status_code
    else:
        return None


def api_login():
    get_acces_token = requests.post(login_endpoint, data={
        'email': email,
        'password': password
    })

    if get_acces_token.status_code == 200:
        access_token = get_acces_token.json()['access_token']
        token_type = get_acces_token.json()['token_type']
        cache.set('access_token', access_token, 21600)
        cache.set('token_type', token_type, 21600)
    else:
        return None
