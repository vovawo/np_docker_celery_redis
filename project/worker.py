import os
import requests
import json
import redis

from celery import Celery
from celery.schedules import crontab

from utility.warehouses import warehouses_sort


celery = Celery()
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

redis_host = os.environ.get("REDIS_HOST")
redis_port = os.environ.get("REDIS_PORT")
np_api_key = os.environ.get("NP_API_KEY")
np_url_api = os.environ.get("NP_URL_API")
np_time_update = json.loads(os.environ.get("NP_TIME_WAREHOUSE_UPDATE"))


@celery.task(name="take_nova_pochta_list")
def take_nova_pochta_list():
    headers = {
        'content-type': 'application/json'
    }
    data = {
        "apiKey": np_api_key,
        "modelName": "AddressGeneral",
        "calledMethod": "getWarehouses",
    }

    warehouses_list = requests.post(np_url_api, data=json.dumps(data), headers=headers).json()['data']

    warehouses_ukr, warehouses_ru = warehouses_sort(warehouses_list)

    r = redis.StrictRedis(host=redis_host, port=redis_port)

    r.execute_command('JSON.SET', "warehouses_ukr", '.', json.dumps(warehouses_ukr))


take_nova_pochta_list.apply()


celery.conf.beat_schedule = {
    'update-np-warehouses': {
        'task': 'take_nova_pochta_list',
        'schedule': crontab(hour=np_time_update['hour'], minute=np_time_update['minute'])
    },
}

celery.conf.timezone = 'Europe/Kiev'
