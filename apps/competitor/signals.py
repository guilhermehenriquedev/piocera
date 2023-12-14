from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from radical.utils.utils import send_email
from .models import RegistrationDocuments, CompetitorsRegistration


# @receiver(post_save, sender=RegistrationDocuments)
# def send_email_registration_document_status_change(sender, instance, created,
#                                                    **kwargs):
#     if not created and instance.approval_status_changed:
#         email_type = 'change_status'
#         document_type = instance.document_type.title
#         document_status = instance.get_approval_status_display()
#         competitor = instance.user.first_name
#         template = 'competitor/email_template.html'
#         html = render_to_string(template, locals())
#         plain_message = strip_tags(html)
#         send_email(
#             subject='Mudança de Status - Documentação',
#             message=plain_message,
#             html_message=html,
#             recipient_list=[instance.user.email],
#         )
#     else:
#         email_type = 'sent_document'
#         competitor = instance.user.first_name
#         template = 'competitor/email_template.html'
#         html = render_to_string(template, locals())
#         plain_message = strip_tags(html)
#         send_email(
#             subject='Recebimento e Análise da Documentação - Rally Piocera/Cerapió',
#             message=plain_message,
#             html_message=html,
#             recipient_list=[instance.user.email]
#         )
import threading
from radical.utils.utils import send_email, send_email_async

@receiver(post_save, sender=CompetitorsRegistration)
def send_email_competitor_registration(sender, instance, created, **kwargs):
    if created:
        competitor = instance.user.first_name
        email_type = 'registration'
        template = 'email/email_template.html'
        html = render_to_string(template, {'email_type': email_type, 'competitor': competitor})
        plain_message = strip_tags(html)
        # send_email(
        #     subject='Confirmação de Inscrição',
        #     message=plain_message,
        #     html_message=html,
        #     recipient_list=[instance.user.email]
        # )
        threading.Thread(
            target=send_email,
            kwargs={
                "subject": 'Confirmação de Inscrição',
                "message": plain_message,
                "html_message": html,
                "recipient_list": [instance.user.email]
            }).start()

        template = 'email/competitor_dados.html'
        competitor_name = instance.user.first_name + ' ' + instance.user.last_name
        html = render_to_string(template,
                                {'competitor_name': competitor_name, 'competitor': instance})
        plain_message = strip_tags(html)

        threading.Thread(
            target=send_email_async,
            kwargs={
                "subject": 'Dados de Inscrição Completos',
                "message": plain_message,
                "html_message": html,
                "recipient_list": ['radicalproducoes1@gmail.com']
            }).start()

