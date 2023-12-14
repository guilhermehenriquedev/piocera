import os

from autoslug.settings import slugify
from django.db import models
from radical.utils.utils import CHOICE_EDITION_STATUS


def get_path_photo_album(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.normcase(
        os.path.join(
            'image_bank',
            'album',
            str(instance.subalbum.album.edition.ano),
            slugify(instance.name[:60]) + '.' + ext))


class Album(models.Model):
    edition = models.ForeignKey('competition.Edition', on_delete=models.CASCADE, verbose_name="Edição")
    order = models.IntegerField('Ordem', null='True', blank="True")
    name = models.CharField('Nome', max_length=200)
    date = models.DateField("Data", null=True, blank=True)
    status = models.PositiveIntegerField('Status', choices=CHOICE_EDITION_STATUS, default=1)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Categoria do album'
        verbose_name_plural = 'Categorias dos albuns'
        ordering = ("order", )

    def __str__(self) -> str:
        return self.name


class SubAlbum(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, verbose_name="Categoria")
    order = models.IntegerField('Ordem', null='True', blank="True")
    name = models.CharField('Nome', max_length=200)
    status = models.PositiveIntegerField('Status', choices=CHOICE_EDITION_STATUS, default=1)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = 'Albuns'
        ordering = ("order", )

    def __str__(self) -> str:
        return self.name


class Photos(models.Model):
    subalbum = models.ForeignKey(SubAlbum, on_delete=models.CASCADE, verbose_name="Album", blank=True, null=True)
    name = models.CharField('Nome', max_length=200)
    photo = models.ImageField('Foto', upload_to=get_path_photo_album, max_length=100)
    legend = models.CharField('Legenda', max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Foto'
        verbose_name_plural = 'Fotos'

    def __str__(self) -> str:
        return self.name
