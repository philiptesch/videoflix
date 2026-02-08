from django.apps import AppConfig


class VideoAppConfig(AppConfig):
    name = 'video_app'


    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
           from . import signals