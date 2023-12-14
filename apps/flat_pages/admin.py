from django.contrib import admin
from django.db import models

from radical.utils.widgets import CharsLeftInput
from .models import Page, CategoryPage, PageFiles


class PageFilesInline(admin.TabularInline):
    model = PageFiles


@admin.register(Page)
class AdminPage(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {
            'widget': CharsLeftInput()
        },
    }

    class Media(admin.ModelAdmin):
        js = ("/static/ckeditor/ckeditor/ckeditor.js",
              "/static/ckeditor/ckeditor-init.js"
              )

    list_display = ['edition', 'title', 'menu_category', 'position', 'status']
    list_display_links = ['edition', 'title']
    search_fields = ['title']
    list_filter = ('menu_category', 'status')
    fields = ['edition', 'menu_category', 'title', 'content', 'external_link','position', 'status']
    inlines = [PageFilesInline]


@admin.register(CategoryPage)
class AdminCategoryPage(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ('is_active',)