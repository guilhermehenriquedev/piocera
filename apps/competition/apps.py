from django.apps import AppConfig


class CompetitionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'competition'
    verbose_name = "Competição"
    verbose_name_plural = "Competições"
    class_icon = 'fas fa-trophy' 