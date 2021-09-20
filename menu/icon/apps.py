from django.apps import AppConfig


class IconConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'icon'

    def ready(self):
        import icon.signals  # noqa