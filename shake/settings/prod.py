from .common import *  # noqa

DEBUG = False

ALLOWED_HOSTS = ['*']

'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
MEDIA_URL = ''  # When you use Amazon S3, you need to set hostname.
STATIC_URL = ''
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = BROKER_URL
'''
