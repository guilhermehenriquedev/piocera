from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'
    verbose_name = "Informações do site"
    verbose_name_plural = "Informações do site"
    class_icon = 'fas fa-sitemap'