from django.apps import AppConfig


class FlatPagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'flat_pages'
    verbose_name = "Página do site"
    verbose_name_plural = "Páginas do site"
    class_icon = 'fas fa-pager'