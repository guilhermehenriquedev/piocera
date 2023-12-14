import pprint

from django.conf import settings
from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from easy_thumbnails.exceptions import InvalidImageFormatError
from easy_thumbnails.files import get_thumbnailer

from radical.utils.widgets import CharsLeftInput
from .models import (
    Federation, Edition,
    Sponsor, Banner,
    WebSiteEdition,
    CompetitionModality, ModalityEdition,
    CompetitionCategory, CategoryModality
)


class CategoryModalityInline(admin.StackedInline):
    formfield_overrides = {
        models.CharField: {
            'widget': CharsLeftInput()
        },
    }
    model = CategoryModality


class ModalityEditionInline(admin.StackedInline):
    formfield_overrides = {
        models.CharField: {
            'widget': CharsLeftInput()
        },
    }
    model = ModalityEdition


@admin.register(WebSiteEdition)
class WebSiteEditionAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {
            'widget': CharsLeftInput()
        },
    }
    list_display = ['edition', 'number_participants_previous_year', 'number_km_previous_year',
                    'number_days_previous_year']
    list_display_links = ['edition']
    search_fields = ['edition__ano']


@admin.register(Federation)
class FederationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {
            'widget': CharsLeftInput()
        },
    }
    list_display = ['name']
    list_display_links = ['name']
    search_fields = ['name']


from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.contrib import messages




@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {
            'widget': CharsLeftInput()
        },
    }
    inlines = [ModalityEditionInline]
    list_display = ['id','ano', 'type', 'edition_date', 'status']
    list_display_links = ['ano', 'type']
    search_fields = ['ano']
    actions = ['clone_edition']

    def clone_edition(self, request, queryset):
        pprint.pprint(queryset)
        for edition in queryset:
            new_edition = edition.clone()
            # Clone objects related to the edition
            for modality_edition in edition.modalityedition_set.all():
                new_modality_edition = modality_edition.clone(new_edition)
                for category_modality in modality_edition.categorymodality_set.all():
                    category_modality.clone(new_modality_edition)
            self.message_user(request, mark_safe(
                'A edição {} foi clonada com sucesso.<br>'.format(edition.ano)))

    clone_edition.short_description = "Clonar edição selecionada"


@admin.register(CompetitionCategory)
class CompetitionCategoryAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {
            'widget': CharsLeftInput()
        },
    }
    list_display = ['name']
    list_display_links = ['name']
    search_fields = ['name']


@admin.register(CompetitionModality)
class CompetitionModalityAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {
            'widget': CharsLeftInput()
        },
    }
    list_display = ['name', 'slug']
    list_display_links = ['name']
    search_fields = ['name']


@admin.register(ModalityEdition)
class ModalityEditionAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {
            'widget': CharsLeftInput()
        },
    }
    list_display = ['foto_thumbnail', 'edition', 'modality']
    list_display_links = ['edition', 'modality']
    fields = ['edition', 'modality', 'description', 'type_competitors', 'documents', 'foto', 'whatsapp_group']
    inlines = [CategoryModalityInline]

    def foto_thumbnail(self, instance):
        try:
            thumbnailer = get_thumbnailer(instance.foto)

            return mark_safe("<img src='{}{}' width='120' />".format(settings.MEDIA_URL,
                                                                     thumbnailer.get_thumbnail({'size': (120, 0)})))
        except OSError:
            return mark_safe("<img src='http://placehold.it/100x80&text=Sem+Imagem' width='120' height='80'/>")

        except InvalidImageFormatError:
            return mark_safe("<img src='http://placehold.it/100x80&text=Imagem+Invalida' width='120' height='80'/>")

    foto_thumbnail.short_description = "Imagem de destaque"


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {
            'widget': CharsLeftInput()
        },
    }
    list_display = ['banner_thumbnail', 'edition', 'position', 'title', 'order','is_active']
    list_display_links = ['banner_thumbnail', 'edition', 'position']
    search_fields = ['title', 'edition__ano']
    fields = ['edition', 'position', 'title', 'banner', 'order', 'start_date', 'end_date', 'is_active']

    # noinspection DjangoSafeString
    def banner_thumbnail(self, instance):
        try:
            thumbnailer = get_thumbnailer(instance.banner)

            return mark_safe("<img src='{}{}' width='120' />".format(settings.MEDIA_URL,
                                                                     thumbnailer.get_thumbnail({'size': (120, 0)})))
        except OSError:
            return mark_safe("<img src='http://placehold.it/100x80&text=Sem+Imagem' width='120' height='80'/>")

        except InvalidImageFormatError:
            return mark_safe("<img src='http://placehold.it/100x80&text=Imagem+Invalida' width='120' height='80'/>")

    banner_thumbnail.short_description = "Banner"


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {
            'widget': CharsLeftInput()
        },
    }
    list_display = ['logo_thumbnail', 'banner_thumbnail', 'edition', 'name', 'type']
    list_display_links = ['logo_thumbnail', 'banner_thumbnail', 'edition']
    fields = ['edition', 'type', 'name', 'logo', 'banner']
    search_fields = ['edition__ano', 'name']

    def logo_thumbnail(self, instance):
        try:
            thumbnailer = get_thumbnailer(instance.logo)

            return mark_safe("<img src='{}{}' width='120' />".format(settings.MEDIA_URL,
                                                                     thumbnailer.get_thumbnail({'size': (120, 0)})))
        except OSError:
            return mark_safe("<img src='http://placehold.it/100x80&text=Sem+Imagem' width='120' height='80'/>")

        except InvalidImageFormatError:
            return mark_safe("<img src='http://placehold.it/100x80&text=Imagem+Invalida' width='120' height='80'/>")

    logo_thumbnail.short_description = "Logotipo"

    def banner_thumbnail(self, instance):
        try:
            thumbnailer = get_thumbnailer(instance.banner)

            return mark_safe("<img src='{}{}' width='120' />".format(settings.MEDIA_URL,
                                                                     thumbnailer.get_thumbnail({'size': (120, 0)})))
        except OSError:
            return mark_safe("<img src='http://placehold.it/100x80&text=Sem+Imagem' width='120' height='80'/>")

        except InvalidImageFormatError:
            return mark_safe("<img src='http://placehold.it/100x80&text=Imagem+Invalida' width='120' height='80'/>")

    banner_thumbnail.short_description = "Banner"
