from functools import partial

from ckeditor.widgets import CKEditorWidget
from django.conf import settings
from django.contrib import admin, messages
from django.db import models
from django import forms
from django.forms import modelform_factory
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.safestring import mark_safe
from easy_thumbnails.exceptions import InvalidImageFormatError
from easy_thumbnails.files import get_thumbnailer

from radical.utils.widgets import CharsLeftInput
from .models import CategoryNews, News


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'


class NewsChangeForm(NewsForm):
    content = forms.CharField(widget=CKEditorWidget(config_name='disable'), label='Conteúdo')


@admin.register(News)
class AdminNews(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {
            'widget': CharsLeftInput()
        },
    }
    list_display = ['cover_thumbnail', 'edition', 'title', 'category', 'status']
    list_display_links = ['cover_thumbnail', 'edition', 'title']
    search_fields = ['title']
    fields = ['edition', 'category', 'title', 'content', 'cover', 'publication_date', 'status', 'author']
    readonly_fields = ['author']

    # noinspection DjangoSafeString
    def cover_thumbnail(self, instance):
        try:
            thumbnailer = get_thumbnailer(instance.cover)

            return mark_safe("<img src='{}{}' width='120' />".format(settings.MEDIA_URL,
                                                                     thumbnailer.get_thumbnail({'size': (120, 0)})))
        except OSError:
            return mark_safe("<img src='http://placehold.it/100x80&text=Sem+Imagem' width='120' height='80'/>")

        except InvalidImageFormatError:
            return mark_safe("<img src='http://placehold.it/100x80&text=Imagem+Invalida' width='120' height='80'/>")

    cover_thumbnail.short_description = "Imagem de destaque"

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.author != request.user:
            readonly_fields = ['edition', 'category', 'title', 'cover', 'publication_date', 'status', 'author']
        else:
            readonly_fields = self.readonly_fields
        return readonly_fields

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = NewsForm
        if change:
            if obj and obj.author != request.user:
                form = NewsChangeForm

        defaults = {
            'form': form,
            'formfield_callback': partial(self.formfield_for_dbfield, request=request),
            **kwargs,
        }
        return modelform_factory(self.model, **defaults)

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_at = timezone.now()
            obj.updated_by = request.user
            old_author = News.objects.get(id=obj.id).author
            if old_author == request.user:
                obj.author = request.user
                obj.save()
        else:
            obj.created_by = request.user
            obj.author = request.user
            obj.save()



@admin.register(CategoryNews)
class AdminCategoryNews(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ('is_active',)
