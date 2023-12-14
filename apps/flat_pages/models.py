import os

from autoslug import AutoSlugField
from autoslug.settings import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse

from radical.utils.utils import CHOICE_EDITION_STATUS

from tinymce.models import HTMLField

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def get_path_archive_page(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.normcase(
        os.path.join(
            'page',
            slugify(instance.name[:60]) + '.' + ext))


class CategoryPage(models.Model):
    name = models.CharField('Nome', max_length=200)
    slug = AutoSlugField(verbose_name='Link', populate_from='name', unique=True, max_length=150, db_index=True,
                         default=1)
    is_active = models.BooleanField('Ativo?', default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Categoria da página'
        verbose_name_plural = 'Categorias das páginas'

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(CategoryPage, self).save(*args, **kwargs)


class Page(models.Model):
    edition = models.ForeignKey('competition.Edition', on_delete=models.CASCADE, verbose_name="Edição")
    title = models.CharField('Título', max_length=200)
    menu_category = models.ForeignKey(CategoryPage, verbose_name='Categoria do menu', on_delete=models.SET_NULL,
                                      null=True)
    
    content = HTMLField(verbose_name='Texto', blank=True, null=True)
    external_link = models.URLField('Link Externo', blank=True, null=True)
    slug = AutoSlugField(verbose_name='Link', populate_from='title', unique=True, max_length=150, db_index=True)
    status = models.PositiveIntegerField('Status', choices=CHOICE_EDITION_STATUS, default=1)
    position = models.PositiveIntegerField("Ordem / Posição", default=0,
                                           help_text='Irá ser usado para ordenação nos submenus')
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')
    

    class Meta:
        verbose_name = 'Página'
        verbose_name_plural = 'Páginas'

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('flatpage_detail', kwargs={'ano': self.edition.ano, 'slug': self.slug})
    

class PageFiles(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nome do arquivo')
    description = models.CharField(max_length=255, verbose_name='Descrição do arquivo')
    file = models.FileField(upload_to=get_path_archive_page, verbose_name='Arquivo')
    page = models.ForeignKey('flat_pages.Page', on_delete=models.CASCADE, verbose_name='Página')

    class Meta:
        verbose_name = 'Arquivos da Página'
        verbose_name_plural = 'Arquivos da Páginas'

    def __str__(self) -> str:
        return self.name