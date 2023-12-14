import uuid
from _decimal import Decimal

from autoslug import AutoSlugField
from autoslug.settings import slugify
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone

from financial.utils import calcula_juros_asaas

PAYMENT_FORM = (
    ('CREDIT_CARD', 'Cartão de Crédito'),
    ('BOLETO', 'Boleto'),
    ('PIX', 'Pix'),
    ('CHAMPION', 'Vencedor do ultimo campeonato'),
    ('CORTESIA', 'Cortesia'),
)


def get_due_date():
    formatted_datetime = (timezone.now() + timezone.timedelta(days=7)).date()
    json_datatime = formatted_datetime.isoformat()
    return json_datatime


class ActivatedManager(models.Manager):
    def get_queryset(self):
        """
        Essa função por padrão retornará apenas lotes válidos
        """
        return super(ActivatedManager, self).get_queryset().filter(
            start_date__lt=timezone.now(),
            end_date__gt=timezone.now()
        )


class InstallmentManager(models.Manager):
    def payment_installment(self, lot):
        parcelas = []
        valor_total = lot.price
        num_parcelas = 12  # máximo de 12 parcelas

        for parcela in range(1, num_parcelas + 1):
            # calculo sem antecipação
            valor_total_com_juros = calcula_juros_asaas(valor_total)

            valor_parcela = valor_total_com_juros / parcela
            parcelas.append({
                'parcela': parcela,
                'valor': round(valor_parcela, 2)
            })
        return parcelas


class Lot(models.Model):
    category_modality = models.ForeignKey("competition.CategoryModality", on_delete=models.CASCADE,
                                          verbose_name='Categoria-Modalidade')
    price = models.DecimalField('Valor', decimal_places=2, max_digits=10, default=0)
    installment_price = models.DecimalField('Valor do parcelamento', decimal_places=2, max_digits=10, default=0)
    number_of_installment = models.IntegerField('Quantidade de parcelas', default=1)
    name = models.CharField('Nome', max_length=100, null=True)
    start_date = models.DateTimeField("Data de início", auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField("Data de encerramento", auto_now=False, auto_now_add=False)
    slug = AutoSlugField(verbose_name='Link', populate_from='name', unique=True, max_length=150, db_index=True,
                         default=1)

    objects = models.Manager()
    lots = ActivatedManager()
    installments = InstallmentManager()
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'

    def __str__(self) -> str:
        return f'{str(self.name)}-{str(self.category_modality)}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Lot, self).save(*args, **kwargs)

    def lot_valido(self):
        valido = True
        if self.start_date > timezone.now() or self.end_date < timezone.now():
            valido = False
        return valido


class LotModel(models.Model):
    name = models.CharField('Nome do modelo', max_length=100)
    quantity_lots = models.IntegerField('Quantidade de lotes',
                                        help_text='Quantidade de lotes a ser gerado automaticamente', default=3)
    price = models.DecimalField('Valor', help_text='Valor do lote em R$', decimal_places=2, max_digits=10, default=0)
    percentage_accretion = models.DecimalField('% de acréscimo',
                                               help_text='Quantidade de acrescimo quando for liberado o próximo lote',
                                               decimal_places=2, max_digits=10, default=0)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Modelo de lote'
        verbose_name_plural = 'Modelos de lote'

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        (1, "Aberto"),
        (2, "Concluido"),
        (3, "Cancelado"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    registration = models.OneToOneField('competitor.Registration', verbose_name='Inscrição', on_delete=models.CASCADE)
    lot = models.ForeignKey('financial.Lot', on_delete=models.CASCADE, verbose_name='Lote')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name='Status')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return "Pedido #{} - {}".format(self.id, self.registration)

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()


class PaymentHistory(models.Model):
    TRANSACTION_STATUS = (
        ('PENDING', 'Cobrança aguardando pagamento'),
        ('CONFIRMED', 'Cobrança Confirmada'),
        ('RECEIVED', 'Cobrança Recebida'),
        ('RECEIVED_IN_CASH', 'Cobrança Recebida em Dinheiro'),
        ('OVERDUE', 'Cobrança Atrasada'),
        ('REFUND_REQUESTED', 'Estorno Solicitado'),
        ('REFUNDED', 'Cobrança Estornada'),
        ('CHARGEBACK_REQUESTED', 'Recebido chargeback'),
        ('CHARGEBACK_DISPUTE', 'Em disputa de chargeback'),
        ('AWAITING_CHARGEBACK_REVERSAL', 'Disputa vencida, aguardando repasse da adquirente'),
        ('DUNNING_REQUESTED', 'Em processo de recuperação'),
        ('DUNNING_RECEIVED', 'Recuperada'),
        ('AWAITING_RISK_ANALYSIS', 'Pagamento em análise'),
        ('DECLINED', 'Pagamento recusado'),
        ('CANCELED', 'Pagamento cancelado'),

    )

    transaction_date = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    order = models.ForeignKey('financial.Order', verbose_name='Criado por', on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(verbose_name='Valor', decimal_places=2, max_digits=15, default=0.00)
    split_condictions = models.PositiveIntegerField(validators=[MaxValueValidator(12)], verbose_name='Parcelas',
                                                    default=0,
                                                    help_text='As condições de parcelamento se referem ao pagamento pelo cartão de crédito')
    transaction_status = models.CharField(verbose_name='Status da Transação', default='PENDING',
                                          choices=TRANSACTION_STATUS, max_length=28)
    transaction_code = models.CharField(verbose_name='ID Pagamento Asaas', max_length=100, null=True, blank=True)
    invoice_url = models.URLField(max_length=240, verbose_name='Url de Pagamento', null=True, blank=True)
    due_date = models.DateField(verbose_name='Data de Vencimento', default=get_due_date)
    bank_slip_url = models.URLField(max_length=240, verbose_name='Url do Boleto', null=True, blank=True)
    invoice_number = models.CharField(max_length=240, verbose_name='Número do pedido', null=True, blank=True)
    billing_type = models.CharField(max_length=15, verbose_name='Método de pagamento', choices=PAYMENT_FORM,
                                    null=True, blank=True)
    qrcode_image = models.TextField(null=True, blank=True)
    qrcode_key = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Histórico de Pagamento'
        verbose_name_plural = 'Históricos de Pagamentos'
        ordering = ['-id']

    def __str__(self):
        return "Pagamento {}".format(self.id)

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()

    def get_type_payments(self, type_value):
        if type_value == 'BOLETO':
            string = 'boleto'
        else:
            string = 'credit_card'
        return "{}".format(self.get_value()[string])

    def subtotal(self):
        return self.amount

    def get_value(self):
        '''
        Boleto = valor do plano
        Cartão a vista = Valor do plano
        Cartão parcelado = (Valor do plano)/ qtd de parcelas
        '''

        val_boleto = Decimal(str(self.subtotal()))
        val_credit_card = Decimal(str(self.subtotal()))

        context = {
            'boleto': val_boleto,
            'credit_card': val_credit_card,
        }

        val_credit_card_split = Decimal(str(self.subtotal()))

        try:
            if val_credit_card_split > 0:
                val_per_split = val_credit_card_split / self.split_condictions
            else:
                val_per_split = 0
        except ZeroDivisionError:
            val_per_split = 0

        context.update({
            'credit_card_split': val_credit_card_split,
            'val_per_split': val_per_split,
        })

        return context


class AccountBank(models.Model):
    ACCOUNT_TYPE = (
        (1, 'Poupança'),
        (2, 'Corrente')
    )
    TYPE_DOCUMENT = (
        (1, 'CNPJ'),
        (2, 'CPF'),
    )

    bank_name = models.CharField(verbose_name='Nome do banco', max_length=80)
    bank_number = models.PositiveIntegerField(verbose_name='Número do banco')
    agency = models.CharField(verbose_name='Agência', max_length=15)
    account_number = models.CharField(verbose_name="Número da conta", max_length=25)
    account_type = models.PositiveIntegerField(verbose_name='Tipo da conta', choices=ACCOUNT_TYPE, default=2)
    phone_for_send_comprovation = models.CharField(verbose_name='Telefone para envio de comprovante', max_length=30)
    document = models.CharField(verbose_name='Número de documento do responsável da conta', max_length=20)
    type_document = models.PositiveIntegerField(verbose_name='Tipo de documento', default=1, choices=TYPE_DOCUMENT)
    is_active = models.BooleanField(verbose_name='Conta ativa para recebimento?',
                                    help_text='Se marcada as outras contas principais serão desativadas para recebimento',
                                    default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Conta bancária'
        verbose_name_plural = 'Contas bancárias'

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()

    def save(self, *args, **kwargs):
        if self.is_active:
            AccountBank.objects.all().update(is_active=False)
        super(AccountBank, self).save(*args, **kwargs)

    def __str__(self):
        return self.bank_name
