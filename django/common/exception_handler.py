from rest_framework.views import exceptions
from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response


def custom_exception_handler(exc, context):

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        data = {
            'code': 20001,
            'message': exc.detail
        }

        return Response(data)

    return None
