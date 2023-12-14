from django import template

from competition.models import Edition
from radical.utils.utils import define_logo

register = template.Library()

@register.filter
def get_pages_for_category(category_pages_with_pages, category_page):
    return category_pages_with_pages.get(category_page, [])

@register.filter()
def get_month_name(month):
    names_dict = {
        '1': 'JAN',
        '2': 'FEV',
        '3': 'MAR',
        '4': 'ABR',
        '5': 'MAI',
        '6': 'JUN',
        '7': 'JUL',
        '8': 'AGO',
        '9': 'SET',
        '10': 'OUT',
        '11': 'NOV',
        '12': 'DEZ',
    }

    return names_dict.get(str(month))


@register.simple_tag()
def logo(request, ano_edition=None):
    try:
        edition = Edition.objects.get(ano=ano_edition)
    except Edition.DoesNotExist:
        edition = Edition.objects.latest('ano')
    logos = define_logo(request, edition.type)
    return logos
