from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from financial.models import PAYMENT_FORM


class CreditCardForm(forms.Form):
    number_credit_card = forms.CharField(label='Número do Cartão', required=True, max_length=19,
                                         widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text',
                                                                       'data-mask': '0000 0000 0000 0000'}))
    cvv = forms.CharField(label='CVV', required=True, max_length=3,
                          widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    expiration_date = forms.CharField(label='Válido até', required=True, max_length=7,
                                      widget=forms.TextInput(
                                          attrs={'class': 'form-control', 'type': 'text', 'data-mask': '00/0000'}))
    hold_name = forms.CharField(label='Nome', required=True, max_length=50,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    split_condictions = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])


class CreditCardHolderInfo(forms.Form):
    name = forms.CharField(label='Nome do titular do cartão', required=True, max_length=50,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    email = forms.CharField(label='Email do titular do cartão', required=True, max_length=50,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    cpfCnpj = forms.CharField(label='CPF ou CNPJ do titular do cartão', required=True, max_length=50,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    postalCode = forms.CharField(label='CEP do titular do cartão', required=True, max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    addressNumber = forms.CharField(label='Número do endereço do titular do cartão', required=True, max_length=50,
                                    widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    addressComplement = forms.CharField(label='Complemento do endereço do titular do cartão', required=False, max_length=50,
                                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    phone = forms.CharField(label='Fone com DDD do titular do cartão', required=True, max_length=50,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    mobilePhone = forms.CharField(label='Fone celular do titular do cartão', required=False, max_length=50,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))


class OrderForm(forms.Form):
    payment_form = forms.CharField(label='Forma de Pagamento', required=True, initial='CREDIT_CARD',
                                   widget=forms.Select(choices=PAYMENT_FORM, ))
