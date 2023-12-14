from datetime import datetime

from django.conf import settings

from flat_pages.models import CategoryPage, Page
from news.models import CategoryNews
from competition.models import Edition


def config(request):
    return {
        'STATIC_URL': settings.STATIC_URL,
        'MEDIA_URL': settings.MEDIA_URL,
    }


def menu_pages(request):
    menu = CategoryPage.objects.filter(is_active=True)
    category_pages_with_pages = {}

    for category_page in menu:
        # Retrieve the related pages with status=3 for each CategoryPage
        pages_with_status_3 = category_page.page_set.filter(status=3)
        category_pages_with_pages[category_page] = pages_with_status_3

    pages_all = Page.objects.filter(status=3)
    pages_evento = pages_all.filter(menu_category__slug__in=['o-evento', 'evento']).order_by('position')
    pages_viagens = pages_all.filter(menu_category__slug__in=['agencia-de-viagens', 'viagens']).order_by('position')
    pages_competidor = pages_all.filter(menu_category__slug__in=['competidor', 'area-do-competidor']).order_by(
        'position')
    return {
        'MENU': menu,
        'category_pages_with_pages': category_pages_with_pages,
        'PAGES': pages_all,
        'PAGES_EVENTO': pages_evento,
        'PAGES_VIAGENS': pages_viagens,
        'PAGES_COMPETIDOR': pages_competidor,
    }


def menu_news(request):
    menu = CategoryNews.objects.filter(is_active=True)
    return {
        'MENU_NEWS': menu,
    }


def current_edition(request):
    try:
        edition = Edition.objects.filter(status=3).latest('ano')
    except Edition.DoesNotExist:
        edition = None
    return {
        'CURRENT_EDITION': edition,
    }
