# coding=utf-8
import pprint
import requests
from django.conf import settings


def create_client(instance):
    values = {
        "name": instance.get_full_name(),
        "email": instance.email,
    }
    url = settings.ASAAS_API_URL + '/customers'
    request = requests.post(url=url, json=values, headers=settings.HEADERS)
    response = request.json()
    return response


def update_client(instance):
    values = {
        "id": instance.customer,
        "name": instance.get_full_name(),
        "email": instance.email,
        "mobilePhone": instance.phone,
        "cpfCnpj": instance.cpf,
    }
    url = settings.ASAAS_API_URL + '/customers'
    request = requests.put(url,
                           json=values,
                           headers=settings.HEADERS)
    response = request.json()
    return response


def delete_client(customer_id):
    values = {"id": customer_id}
    url = settings.ASAAS_API_URL + '/customers'
    request = requests.delete(url, json=values,
                              headers=settings.HEADERS)
    response = request.json()
    return response