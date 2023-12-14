from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
    verbose_name = "Notícia"
    verbose_name_plural = "Notícias"
    class_icon = 'fas fa-newspaper'