import requests
import re
import time
import os
from django.conf import settings
import gitlab

access_token = settings.GITLAB_ACCESS_KEY
gitlab_server = settings.GITLAB_SERVER 


def trigger_pipeline(project_id, trigger_token, ref, **kwargs):
    '''
    kwargs variables key-valued must strings.
    '''

    gl = gitlab.Gitlab(gitlab_server, private_token=access_token)
    project = gl.projects.get(project_id)
    pipeline = project.trigger_pipeline(
        ref=ref, token=trigger_token, variables=kwargs)

    return pipeline
