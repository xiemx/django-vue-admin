from celery.task.control import inspect
from django.http.response import HttpResponse
import json


def fetch_celery_registered_tasks(request, *args, **kwargs):
    i = inspect()
    return HttpResponse(json.dumps(i.registered_tasks()))
