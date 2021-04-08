from celery import Task
from django.conf import settings


class Callback(Task):

    def on_success(self, retval, task_id, args, kwargs):
        print('task success')

    def on_retry(self, exc, task_id, args, kwargs):
        print('task retry')

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('task failure')

    def run(self, *args, **kwargs):
        """The body of the task executed by workers."""
        print('------------run')
        super().run(*args, **kwargs)
        raise NotImplementedError('Tasks must define the run method.')

    def after_return(self, *args, **kwargs):
        print('------------after_return')
        super().after_return(*args, **kwargs)

    def delay(self, *args, **kwargs):
        print('----------------delay')
        super().delay(*args, **kwargs)
