from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe

from radical.utils.widgets import CharsLeftInput
from .models import (
    Team, Registration,
    Document, RegistrationDocuments,
    CompetitorsRegistration, TypeCompetitor, VehicleBrand, VehicleModel, TireBrand, TeamMembers, CheckList,
    CheckListItem, CompetitorCheckList, Boleto, CompetitorCheckListItem
)


class CompetitorsRegistrationItemInline(admin.StackedInline):
    model = CompetitorsRegistration
    extra = 0


class TeamMembersInline(admin.TabularInline):
    model = TeamMembers


class RegistrationDocumentsInlineInline(admin.TabularInline):
    model = RegistrationDocuments
    extra = 0


class BoletoInlineInline(admin.TabularInline):
    model = Boleto
    extra = 0


@admin.register(Boleto)
class BoletoAdmin(admin.ModelAdmin):
    list_display = ['id', 'competitor_registration', 'document_file']
    list_display_links = ['id', 'competitor_registration', 'document_file']
    search_fields = ['competitor_registration__user__first_name', 'competitor_registration__user__last_name']


@admin.register(VehicleBrand)
class VehicleBrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
    list_display_links = ['name']
    search_fields = ['name']


@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
    list_display_links = ['name']
    search_fields = ['name']


@admin.register(TireBrand)
class TireBrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
    list_display_links = ['name']
    search_fields = ['name']


@admin.register(TypeCompetitor)
class TypeCompetitorAdmin(admin.ModelAdmin):
    pass


@admin.register(RegistrationDocuments)
class RegistrationDocumentsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {
            'widget': CharsLeftInput()
        },
    }
    list_display = ['competitor_registration', 'user', 'document_type', 'archive_link', 'approval_status']
    search_fields = ['user__first_name']

    # noinspection DjangoSafeString
    def archive_link(self, instance):
        return mark_safe(
            "<a href='{}{}' target='_blank'> Abrir arquivo </a>".format(settings.MEDIA_URL, instance.document_file))

    archive_link.short_description = "Documento"


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {
            'widget': CharsLeftInput()
        },
    }
    list_display = ['title', 'model_archive', 'slug']
    search_fields = ['title']
    actions = ['create_slug']

    def create_slug(self, request, queryset):
        update_count = 0
        for document in queryset:
            document.title = document.title
            document.save()
            update_count += 1
        self.message_user(request, mark_safe(
            'Documentos {} tiram suas slugs alteradas.<br>'.format(update_count)))

    create_slug.short_description = "Gera uma slug automaticamente para os documentos selecionados"

    # noinspection DjangoSafeString
    def model_archive(self, instance):
        return mark_safe(
            "<a href='{}{}' target='_blank'> Abrir arquivo </a>".format(settings.MEDIA_URL, instance.model))

    model_archive.short_description = "Modelo de documento"


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {
            'widget': CharsLeftInput()
        },
    }
    list_display = ['name', 'coordinator']
    list_display_links = ['name']
    search_fields = ['name', 'coordinator__first_name']
    inlines = [TeamMembersInline]


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {
            'widget': CharsLeftInput()
        },
    }
    list_display = ['user_name','registration_number', 'sponsorship', 'vehicle_brand', 'vehicle_model', 'tire_brand', 'wheel_rim',
                    'lot', ]
    list_display_links = ['user_name','registration_number']
    search_fields = ['sponsorship', 'team__name', 'registration_number']
    fields = ['status', 'sponsorship', 'vehicle_brand', 'vehicle_model', 'tire_brand', 'wheel_rim', 'lot', 'team',
              'has_team',
              'payment_status', 'registration_number']
    readonly_fields = ['registration_number']
    inlines = [CompetitorsRegistrationItemInline, ]

    def user_name(self, obj):
        registration = obj
        competitor_registration = registration.competitorsregistration_set.all()
        names = []
        for competitor in competitor_registration:
            names.append(f'{competitor.user.first_name} {competitor.user.last_name}')
        return names

    user_name.short_description = 'Usuário'


@admin.register(CompetitorsRegistration)
class CompetitorsRegistrationAdmin(admin.ModelAdmin):
    list_display = ['modality_name', 'category_name', 'registration', 'get_full_name', 'get_email', 'get_phone', 'type',
                    'number',
                    'thermo',
                    'competitor_card']
    list_display_links = ['registration']
    search_fields = ['user__first_name', 'user__last_name', 'user__phone', 'registration__registration_number']
    fields = ['registration', 'user', 'type', 'number', 'thermo', 'competitor_card']
    list_filter = ['competitor_card', ]
    inlines = [RegistrationDocumentsInlineInline, BoletoInlineInline]

    def get_full_name(self, obj):
        # Retorne uma string formatada com os campos relevantes do User
        user = obj.user
        return f'Nome Completo: {user.get_full_name()}'

    get_full_name.short_description = 'Nome Completo'

    def get_email(self, obj):
        # Retorne uma string formatada com os campos relevantes do User
        user = obj.user
        return f'Email: {user.email}'

    get_email.short_description = 'Email'

    def get_phone(self, obj):
        # Retorne uma string formatada com os campos relevantes do User
        user = obj.user
        return f'Telefone: {user.phone}'

    get_phone.short_description = 'Telefone'

    def modality_name(self, obj):
        return obj.registration.lot.category_modality.modality_edition.modality.name

    modality_name.short_description = 'Modalidade'

    def category_name(self, obj):
        return obj.registration.lot.category_modality.category.name

    category_name.short_description = 'Categoria'


@admin.register(CompetitorCheckList)
class CompetitorCheckListAdmin(admin.ModelAdmin):
    list_display = ['competitor_registration', 'check_list', ]


@admin.register(CompetitorCheckListItem)
class CompetitorCheckListItemAdmin(admin.ModelAdmin):
    list_display = ['competitor_checklist', 'check_list_item', 'confirmation_image']


class CheckListItemInline(admin.StackedInline):
    model = CheckListItem
    extra = 0


@admin.register(CheckList)
class CheckListAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    inlines = [CheckListItemInline]


@admin.register(CheckListItem)
class CheckListItemAdmin(admin.ModelAdmin):
    list_display = ['text', ]
