from django.apps import AppConfig


class FinancialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'financial'
    verbose_name = "Financeiro"
    verbose_name_plural = "Financeiros"
    class_icon = 'fas fa-hand-holding-usd'

    def ready(self):
        from . import signals
