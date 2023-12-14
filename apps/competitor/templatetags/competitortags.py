import pprint

from django import template
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from ..models import Document, RegistrationDocuments
from users.models import User
from financial.models import Lot, Order, PaymentHistory, AccountBank
from datetime import datetime

register = template.Library()


@register.simple_tag
def document_file_download(request, document_id, competitor_id):
    try:
        registration_document = RegistrationDocuments.objects.filter(
            document_type=document_id,
            user=competitor_id
        ).latest('created_at')

        if registration_document.approval_status in ['1', '2', '3']:
            return {
                'there_is_registration_document': True,
                'file_link': f'{settings.MEDIA_URL}{registration_document.document_file}'
            }
        else:
            return {'there_is_registration_document': False}
    except ObjectDoesNotExist:
        return {'there_is_registration_document': False}


@register.simple_tag
def display_input(document_id, competitor_id):
    my_dict = {}

    try:
        registration_document = RegistrationDocuments.objects.filter(
            document_type=document_id,
            user=competitor_id
        ).latest('created_at')

        if registration_document.approval_status in ['3']:
            my_dict['show'] = True
            my_dict['status'] = f'Documento {registration_document.get_approval_status_display()}'
        elif registration_document.approval_status in ['1', '2']:
            my_dict['show'] = True
            my_dict['status'] = f'Documento {registration_document.get_approval_status_display()}'
        else:
            my_dict['show'] = False
            my_dict['status'] = f'Documento {registration_document.get_approval_status_display()}'

    except ObjectDoesNotExist:
        registration_document = None

    return my_dict


@register.simple_tag
def document_admin(document, competitor):
    try:
        competidor_document = RegistrationDocuments.objects.get(document_type=document,
                                                                user=competitor.user,
                                                                competitor_registration=competitor
                                                                )
    except RegistrationDocuments.DoesNotExist:
        competidor_document = document
    return competidor_document


@register.simple_tag
def get_sorted_registrations(registrations):
    # Ordena as inscrições considerando a presença ou ausência de documentos
    sorted_registrations = sorted(
        registrations,
        key=lambda registration: min_document_date(registration)
    )
    # Adiciona o histórico de pagamento em cada instância de Registration com documentos
    for registration in sorted_registrations:
        try:
            payment_history = PaymentHistory.objects.filter(order=registration.order).latest('created_at')
        except PaymentHistory.DoesNotExist:
            payment_history = PaymentHistory.objects.create(order=registration.order, transaction_status='PENDING')
        registration.history = payment_history
    return sorted_registrations


def min_document_date(registration):
    competitor_registration = registration.competitorsregistration_set.first()

    # Verifica se a inscrição tem documentos associados
    if competitor_registration and competitor_registration.registrationdocuments_set.exists():
        # Encontra a data do documento mais antigo
        oldest_document_date = min(competitor_registration.registrationdocuments_set.all(),
                                   key=lambda doc: doc.created_at).created_at.date()
    else:
        # Caso não tenha documentos, coloca a data muito grande
        oldest_document_date = datetime(9999, 12, 31).date()

    return oldest_document_date


@register.simple_tag
def sort_by_document_created_at(registrations):
    pprint.pprint(registrations)
    all_documents = []

    # Coleta todos os documentos de todas as inscrições em uma lista
    for registration in registrations:
        documents = registration.registrationdocuments_set.all()
        all_documents.extend(documents)
    print(all_documents)
    # Ordena os documentos com base na data de criação
    sorted_documents = sorted(all_documents, key=lambda doc: doc.created_at)

    # Cria uma lista de inscrições reorganizada com base na ordem dos documentos
    sorted_registrations = []
    used_registration_ids = set()
    for document in sorted_documents:
        registration = document.competitor_registration
        if registration.id not in used_registration_ids:
            sorted_registrations.append(registration)
            used_registration_ids.add(registration.id)
    pprint.pprint(sorted_registrations)
    return sorted_registrations

# registration = inscricao.registration
# lot = Lot.objects.get(registration=registration)
# category_modaliti = CategoryModality.objects.get(id=lot.category_modality.id)
# modality_edition = ModalityEdition.objects.get(id=category_modaliti.modality_edition.id)
#
# documentos_modality_edition = modality_edition.documents.all()
# for documento in documentos_modality_edition:
#     registration_document = RegistrationDocuments.objects.filter(document_type=documento,
#                                                                  user=inscricao.user,
#                                                                  competitor_registration=inscricao)
#
#     for doc in registration_document:
#         inscricao.registration_documents_approved.append(doc)
#         if documento == doc.document_type:
#             documento.status = doc.approval_status
#         else:
#             documento.status = '6'
#         if doc.approval_status == '3':
#             inscricao.documents_approved.append(documento)
#     inscricao.documents.append(documento)
