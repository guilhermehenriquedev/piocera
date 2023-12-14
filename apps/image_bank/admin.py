from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from easy_thumbnails.exceptions import InvalidImageFormatError
from easy_thumbnails.files import get_thumbnailer

from .models import (
    Album, Photos, SubAlbum
)


class PhotosInline(admin.TabularInline):
    model = Photos


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['edition', 'name', 'status', 'order']
    search_fields = ['name']


@admin.register(SubAlbum)
class SubAlbumAdmin(admin.ModelAdmin):
    list_display = ['album', 'name', 'status']
    search_fields = ['name']
    inlines = [PhotosInline]


@admin.register(Photos)
class PhotosAdmin(admin.ModelAdmin):
    list_display = ['photo_thumbnail', 'subalbum', 'name']
    list_display_links = ['photo_thumbnail', 'subalbum']
    search_fields = ['name']

    # noinspection DjangoSafeString
    def photo_thumbnail(self, instance):
        try:
            thumbnailer = get_thumbnailer(instance.photo)

            return mark_safe("<img src='{}{}' width='120' />".format(settings.MEDIA_URL,
                                                                     thumbnailer.get_thumbnail({'size': (120, 0)})))
        except OSError:
            return mark_safe("<img src='http://placehold.it/100x80&text=Sem+Imagem' width='120' height='80'/>")

        except InvalidImageFormatError:
            return mark_safe("<img src='http://placehold.it/100x80&text=Imagem+Invalida' width='120' height='80'/>")

    photo_thumbnail.short_description = "Imagem"