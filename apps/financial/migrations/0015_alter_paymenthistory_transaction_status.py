# Generated by Django 4.2 on 2023-05-17 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0014_lot_installment_price_lot_number_of_installment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenthistory',
            name='transaction_status',
            field=models.CharField(choices=[('PENDING', 'Cobrança aguardando pagamento'), ('CONFIRMED', 'Cobrança Confirmada'), ('RECEIVED', 'Cobrança Recebida'), ('RECEIVED_IN_CASH', 'Cobrança Recebida em Dinheiro'), ('OVERDUE', 'Cobrança Atrasada'), ('REFUND_REQUESTED', 'Estorno Solicitado'), ('REFUNDED', 'Cobrança Estornada'), ('CHARGEBACK_REQUESTED', 'Recebido chargeback'), ('CHARGEBACK_DISPUTE', 'Em disputa de chargeback'), ('AWAITING_CHARGEBACK_REVERSAL', 'Disputa vencida, aguardando repasse da adquirente'), ('DUNNING_REQUESTED', 'Em processo de recuperação'), ('DUNNING_RECEIVED', 'Recuperada'), ('AWAITING_RISK_ANALYSIS', 'Pagamento em análise'), ('DECLINED', 'Pagamento em recusado'), ('CANCELED', 'Pagamento em cancelado')], default='PENDING', max_length=28, verbose_name='Status da Transação'),
        ),
    ]
