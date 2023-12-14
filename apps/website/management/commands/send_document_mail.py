from django.core.management.base import BaseCommand
from financial.models import Lot, Order, PaymentHistory, AccountBank
from users.models import User
from competitor.models import Team, Registration, CompetitorsRegistration, \
    Document, RegistrationDocuments, VehicleModel, \
    TeamMembers
from competition.models import CategoryModality, ModalityEdition
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from radical.utils.utils import send_email


class Command(BaseCommand):
    help = 'Esse script envia um email para todos os usuários que não enviaram a documentação.'

    def handle(self, *args, **options):
        for competitor in CompetitorsRegistration.objects.all():
            documents = []
            documents_approved = []
            documents_pending = []
            print("Meu script está sendo executado!")
            lot = Lot.objects.get(registration=competitor.registration)
            category_modality = CategoryModality.objects.get(id=lot.category_modality.id)
            modality_edition = ModalityEdition.objects.get(id=category_modality.modality_edition.id)

            documentos_modality_edition = modality_edition.documents.all()
            for documento in documentos_modality_edition:
                documents.append(documento)
                registration_document = RegistrationDocuments.objects.filter(document_type=documento,
                                                                             user=competitor.user)
                for doc in registration_document:
                    if doc.approval_status == '3':
                        documents_approved.append(documento)
                    else:
                        documents_pending.append(documento)
            if documents_pending:
                email_type = 'documentation_pending'
                template = 'email/email_template.html'
                competitor_name = competitor.user.first_name + ' ' + competitor.user.last_name
                html = render_to_string(template, {'email_type': email_type, 'competitor': competitor_name,
                                                   'list_pending': documents_pending})
                plain_message = strip_tags(html)
                send_email(
                    subject='Documentação Pendente',
                    message=plain_message,
                    html_message=html,
                    recipient_list=[competitor.user.email]
                )
