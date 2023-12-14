import os

from autoslug import AutoSlugField
from autoslug.settings import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.utils import timezone
#testingTinymce
from tinymce.models import HTMLField

from radical.utils.utils import CHOICE_EDITION_STATUS


def get_path_cover_news(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.normcase(
        os.path.join(
            'noticia',
            slugify(instance.title[:60]) + '.' + ext))


class ActivatedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=3, publication_date__lte=timezone.now()).order_by('-created_at')


class CategoryNews(models.Model):
    name = models.CharField('Nome', max_length=200)
    is_active = models.BooleanField('Ativo?', default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Categoria da noticia'
        verbose_name_plural = 'Categorias das noticias'

    def __str__(self) -> str:
        return self.name


class News(models.Model):
    created_by = models.ForeignKey('users.User', verbose_name='Criado por', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_by = models.ForeignKey(
        'users.User',
        verbose_name='Editado por',
        related_name='news_updated_by',
        blank=True, null=True, on_delete=models.CASCADE
    )
    updated_at = models.DateTimeField(verbose_name='Editado em', blank=True, null=True)
    edition = models.ForeignKey('competition.Edition', on_delete=models.CASCADE, verbose_name="Edição")
    title = models.CharField('Título', max_length=200, null=True)
    category = models.ForeignKey(CategoryNews, on_delete=models.CASCADE, verbose_name="Categoria", null=True,
                                 blank=True)
    cover = models.ImageField(verbose_name='Imagem de destaque', upload_to=get_path_cover_news, max_length=100,
                              null=True)
    #content = RichTextUploadingField(config_name='basic', verbose_name='Texto')
    content = HTMLField(verbose_name='Texto')
    publication_date = models.DateTimeField("Data de publicação",
                                            help_text='O sistema só irá liberar quando chegar na data de publicação.',
                                            null=True, blank=True)
    author = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="Autor", related_name='news_autor',
                               null=True, blank=True)
    slug = AutoSlugField(verbose_name='Link', populate_from='title', unique=True, max_length=150, db_index=True)
    status = models.PositiveIntegerField('Status', choices=CHOICE_EDITION_STATUS, default=1)

    objects = models.Manager()
    news = ActivatedManager()

    class Meta:
        verbose_name = 'Notícia'
        verbose_name_plural = 'Notícias'

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('news:postage_detail', kwargs={'ano': int(self.edition.ano), 'slug': self.slug})
