# coding=utf-8
import re
import pytz
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.core.mail import send_mail

# status de edição
CHOICE_EDITION_STATUS = [
    (1, 'RASCUNHO'),
    (3, 'ATIVADA'),
    (2, 'DESATIVADA'),
]


def convert_to_localtime(utctime):
    utc = utctime.replace(tzinfo=pytz.UTC)
    return utc.astimezone(timezone.get_current_timezone())


def escape_link(html):
    """Returns the given HTML with ampersands, quotes and carets encoded."""
    return mark_safe(
        html.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'",
                                                                                                            '&#39;')
    )


def escape_chars(text):
    text = text.replace('&', '&amp;'). \
        replace('<', '&lt;'). \
        replace('>', '&gt;'). \
        replace('"', '&quot;'). \
        replace("'", '\&#39;')

    return text


def default_current_time():
    return timezone.now()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def clear_html(text):
    clear = re.compile('<.*?>')
    cleantext = re.sub(clear, '', text)
    return cleantext


def define_logo(request, edition_type):
    schema = 'https://'
    if settings.DEBUG == True:
        schema = 'http://'

    site = schema + get_current_site(request).domain

    if edition_type == 1:
        # cerapio
        logos = {
            'SITE_LOGO_BRANCA': site + '/static/images/logos/cerapioBranca.png',
            'SITE_LOGO_ESCURO': site + '/static/images/logos/cerapio.png',
            'SITE_LOGO_PALAVRA': site + '/static/images/logos/cerapioPalavraBranca.png',
        }
    else:
        # piocera
        logos = {
            'SITE_LOGO_BRANCA': site + '/static/images/logos/pioceraBranca.png',
            'SITE_LOGO_ESCURO': site + '/static/images/logos/piocera.png',
            'SITE_LOGO_PALAVRA': site + '/static/images/logos/pioceraPalavraBranca.png',
        }

    return logos


def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))


def send_email(subject, message, recipient_list, html_message):
    result = send_mail(
        subject=subject,
        message=message,
        html_message=html_message,
        recipient_list=recipient_list,
        fail_silently=False,
        from_email=None,
    )

    return result


def send_email_async(*args, **kwargs):
    result = send_mail(
        subject=kwargs.get("subject"),
        message=kwargs.get("message"),
        html_message=kwargs.get("html_message"),
        recipient_list=kwargs.get("recipient_list"),
        fail_silently=False,
        from_email=None,
    )

    return result
