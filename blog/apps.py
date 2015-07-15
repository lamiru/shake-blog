from django.apps import AppConfig as DjangoAppConfig
from blog.signals import app_ready


class AppConfig(DjangoAppConfig):
    name = 'blog'
    verbose_name = 'Blog'

    def ready(self):
        app_ready.send(sender=self)
