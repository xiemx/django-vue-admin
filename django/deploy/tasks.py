from celery import shared_task
from django.utils import timezone as datetime
from deploy.models import Release


@shared_task
def DeployService(release_id):
    print("release id", release_id)
    _release = Release.objects.get(id=release_id)
    _release.status = "COMPLETED"
    _release.save()
    print("helm rollback!!!", _release.cluster.name,
          _release.service, _release.namespace, _release.revision, _release)
    return True
