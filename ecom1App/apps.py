from django.apps import AppConfig


class Ecom1AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecom1App'

    def ready(self):
        import ecom1App.signals
