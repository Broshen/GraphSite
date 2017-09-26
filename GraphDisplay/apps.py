from django.apps import AppConfig


class GraphdisplayConfig(AppConfig):
    name = 'GraphDisplay'

    def ready(self):
        import GraphDisplay.signals