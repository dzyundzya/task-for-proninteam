from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    """Configuration class for the Payments application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'server.apps.payments'
    verbose_name = 'Payments'
