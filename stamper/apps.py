from django.apps import AppConfig


class StamperConfig(AppConfig):
    name = 'stamper'

    def ready(self):
        import stamper.signals
