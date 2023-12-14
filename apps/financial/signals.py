import threading

from django.db.models.signals import post_save
from django.dispatch import receiver
from radical.utils.utils import send_email, send_email_async
from .models import PaymentHistory
from competitor.models import CompetitorsRegistration, Registration
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from financial.models import Order

@receiver(post_save, sender=PaymentHistory)
def send_email_competitor_registration(sender, instance, **kwargs):
    if instance.transaction_status == 'CONFIRMED':
        competitors = CompetitorsRegistration.objects.filter(registration=instance.order.registration.id)
        # Atualizar o status do pedido (Order)
        instance.order.status = '2'
        instance.order.save()

        # Atualizar o status do registro (Registration)
        instance.order.registration.status = '2'
        instance.order.registration.payment_status = True
        instance.order.registration.save()
        for competitor in competitors:
            email_list = []
            if competitor.user.email:
                email_list.append(competitor.user.email)
                template = 'financial/email_payment.html'
                competitor_name = competitor.user.first_name + ' ' + competitor.user.last_name
                html = render_to_string(template, {'competitor_name': competitor_name})
                plain_message = strip_tags(html)

                threading.Thread(
                    target=send_email_async,
                    kwargs={
                        "subject": 'Pagamento Recebido',
                        "message": plain_message,
                        "html_message": html,
                        "recipient_list": email_list
                    }).start()

