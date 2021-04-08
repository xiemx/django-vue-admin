import requests
import json
# from rest_framework_jwt.utils import jwt_decode_handler
from django.conf import settings

def get_user_info_for_gitlab(username, token):
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    resp = requests.get(
        '{}/api/v4/users/?username={}'.format(settings.GITLAB_SERVER, username), headers=headers)

    if not resp.json():
        raise Exception("User does not exist.")

    return resp.json()[0]
