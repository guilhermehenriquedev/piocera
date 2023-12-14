import pprint

import requests
import json
from django.conf import settings
from django.utils import timezone


def get_due_date():
    formatted_datetime = timezone.now() + timezone.timedelta(days=7)
    json_datatime = formatted_datetime.isoformat()
    return json_datatime


def create_charge(instance, client, type_payment=None):
    values = {
        "customer": client.customer,
        "billingType": instance.billing_type,
        "dueDate": get_due_date(),
        "description": instance.description,
    }
    if instance.billing_type == 'CREDIT_CARD':
        # Cartão de crédito -> Sem campos adicionais
        values.update({
            "creditCard": {
                "holderName": instance.holderName,
                "number": instance.number,
                "expiryMonth": instance.expiryMonth,
                "expiryYear": instance.expiryYear,
                "ccv": instance.ccv
            },
            "creditCardHolderInfo": {
                "name": instance.name,
                "email": instance.email,
                "cpfCnpj": instance.cpfCnpj,
                "postalCode": instance.postalCode,
                "addressNumber": instance.addressNumber,
                "addressComplement": instance.addressComplement,
                "phone": instance.phone,
                "mobilePhone": instance.mobilePhone
            }
        })
        if type_payment == 3:
            ## Parcelamento
            values.update({
                'installmentCount': instance.split_condictions,
                # 'installmentValue': instance.value_split,
                "totalValue": instance.value,
            })
        else:
            values.update({
                "value": instance.value,
            })
    else:
        # Pix -> Sem campos adicionais
        values.update({
            "value": instance.value,
        })

    return send_charge(values)


def send_charge(values=None):
    url = settings.ASAAS_API_URL + '/payments'
    request = requests.post(url, data=json.dumps(values),
                            headers=settings.HEADERS)
    response = request.json()
    return response


def get_charge(id):
    url = settings.ASAAS_API_URL + '/payments/' + id
    request = requests.get(url, headers=settings.HEADERS)
    response = request.json()
    return response


def gera_pix_key(id):
    url = settings.ASAAS_API_URL + '/payments/' + id + '/pixQrCode'
    # url = settings.ASAAS_API_URL + '/pix/transactions?id=' + id
    request = requests.get(url, headers=settings.HEADERS)
    response = request.json()
    return response
