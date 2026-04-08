from django.apps import AppConfig


class CartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'

    # Переопределяем метод ready, чтобы подключить наши сигналы при старте
    def ready(self):
        import cart.signals
