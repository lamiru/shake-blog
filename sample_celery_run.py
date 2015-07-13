'''
1) execute redis

1) execute celery worker
    shell> python manage.py celery worker
'''

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shake.settings.dev")
import django
django.setup()


from blog.tasks import slow_sum

s = slow_sum.delay(10, 10)
print('task_id : {}'.format(s.task_id))
# http://celery.readthedocs.org/en/latest/reference/celery.result.html#celery.result.AsyncResult.status
print('current status : {}'.format(s.status))
print('waiting for executing ...')

result = s.get()
print('current status : {}'.format(s.status))
print('result : {}'.format(result))
