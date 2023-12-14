# Generated by Django 4.2 on 2023-04-23 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0004_paymenthistory_lot_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lotmodel',
            old_name='model_name',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='lotmodel',
            name='percentage_accretion',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Quantidade de acrescimo quando for liberado o próximo lote', max_digits=10, verbose_name='% de acréscimo'),
        ),
        migrations.AlterField(
            model_name='lotmodel',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Valor do lote em R$', max_digits=10, verbose_name='Valor'),
        ),
        migrations.AlterField(
            model_name='lotmodel',
            name='quantity_lots',
            field=models.IntegerField(default=3, help_text='Quantidade de lotes a ser gerado automaticamente', verbose_name='Quantidade de lotes'),
        ),
    ]
