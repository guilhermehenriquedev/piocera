from django.apps import AppConfig


class ImageBankConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'image_bank'
    verbose_name = "Banco de imagens"
    verbose_name_plural = "Banco de imagens"
    class_icon = 'fas fa-images'