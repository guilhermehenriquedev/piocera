from django.apps import AppConfig


class CompetitorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'competitor'
    verbose_name = "Competidor"
    verbose_name_plural = "Competidores"
    class_icon = 'fas fa-users'

    def ready(self):
        from . import signals
