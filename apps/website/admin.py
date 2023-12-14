from django.contrib import admin
from django.db import models
from radical.utils.widgets import CharsLeftInput
from .models import WebSite, Questions, Champion, Newsletter
from import_export.admin import ImportExportModelAdmin


@admin.register(Newsletter)
class Newsletter(ImportExportModelAdmin):
    list_display = ['email', 'created_at']
    list_display_links = ['email']
    search_fields = ['email']


@admin.register(Champion)
class AdminChampion(admin.ModelAdmin):
    list_display = ['edition', 'modality', 'name', 'category']
    list_display_links = ['modality', 'name', 'category']
    search_fields = ['name', 'modality', 'category', 'edition', 'sponsorship', 'state', 'vehicle']
    list_filter = ('category',)


@admin.register(Questions)
class AdminQuestions(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {
            'widget': CharsLeftInput()
        },
    }
    list_display = ['title', 'is_active']
    list_display_links = ['title']
    search_fields = ['title']
    list_filter = ('is_active',)
    fields = ['title', 'answer', 'is_active']


@admin.register(WebSite)
class AdminWebSite(admin.ModelAdmin):
    formfield_overrides = {
        models.URLField: {
            'widget': CharsLeftInput()
        },
    }
    list_display = ['event_start_date', 'number_of_participants', 'number_of_states', 'number_of_countries']
    list_display_links = ['event_start_date']
