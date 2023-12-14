from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from financial.models import Order, PaymentHistory
from competitor.models import Registration
from competition.models import Federation, CompetitionModality

from financial.models import Lot

from competition.models import Edition

from website.models import Newsletter, Champion

TRANSACTION_STATUS = (
    ('', 'Selecione'),
    ('PENDING', 'Cobrança Pendente'),
    ('CONFIRMED', 'Cobrança Confirmada'),
    ('DECLINED', 'Pagamento Recusado'),
    ('CANCELED', 'Pagamento Cancelado'),
)
CHOICE_STATUS = [
    ('0', 'Selecione'),
    ('1', 'Registro'),
    ('2', 'Pago'),
    ('3', 'Homologado'),
    ('4', 'Cancelado'),
]


class RegistrationAdminForm(forms.ModelForm):
    status = forms.ChoiceField(label='Status do Pagamento', required=True, initial='', choices=CHOICE_STATUS)
    class Meta:
        model = Registration
        fields = ['status', ]


class LotAdminForm(forms.ModelForm):
    lot = forms.ModelChoiceField(queryset=Lot.objects.none(), label='Lote Válido')

    class Meta:
        model = Registration
        fields = ['lot', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lot'].queryset = self.get_lots_validos()

    def get_lots_validos(self):
        lots_validos = Lot.lots.get_queryset().filter(id__in=Lot.objects.values_list('id', flat=True))
        return lots_validos


PAYMENT_FORM = (
    ('', 'Selecione'),
    ('CREDIT_CARD', 'Cartão de Crédito'),
    ('BOLETO', 'Boleto'),
    ('PIX', 'Pix'),
    ('CHAMPION', 'Vencedor do ultimo campeonato'),
    ('CORTESIA', 'Cortesia'),
)


class AdminPaymentForm(forms.ModelForm):
    billing_type = forms.ChoiceField(label='Forma de Pagamento', required=True, initial='',
                                     choices=PAYMENT_FORM, )
    transaction_status = forms.ChoiceField(label='Status do Pagamento', required=True, initial='',
                                           choices=TRANSACTION_STATUS)
    amount = forms.DecimalField(label='Valor', required=True, max_digits=10, decimal_places=2, initial=0.00, )
    split_condictions = forms.IntegerField(label='Parcela', required=True, max_value=12, min_value=1, initial=1, )

    class Meta:
        model = PaymentHistory
        fields = ['billing_type', 'transaction_status', 'amount', 'split_condictions']


class AdminRecuseDocumentForm(forms.Form):
    recuse_reason = forms.CharField(label='Motivo da Recusa', required=True,
                                    widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))


class ChampionEditionForm(forms.Form):
    edition = forms.ChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        super(ChampionEditionForm, self).__init__(*args, **kwargs)
        self.fields['edition'].choices = self.get_edition_choices()

    def get_edition_choices(self):
        choices = Champion.objects.values_list('edition', flat=True).distinct()
        choices = sorted(choices, reverse=True)  # Sort the years in reverse (descending) order
        choices = [('Ano - ' + str(position), 'Ano - ' + str(position)) for position in choices]
        choices.insert(0, ('', 'Exibir todas'))  # Add an empty value to display all champions
        return choices


class NewsletterForm(forms.ModelForm):
    email = forms.EmailField(label='E-mail', required=True)
    interest_area = forms.ModelChoiceField(
        label='Área de Interesse',
        queryset=CompetitionModality.objects.all(),  # Isso obtém todos os objetos de CompetitionModality
        empty_label=None,  # Impede a exibição de uma opção vazia
        required=True
    )

    class Meta:
        model = Newsletter
        fields = ['email', 'interest_area']
