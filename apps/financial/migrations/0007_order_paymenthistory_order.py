# Generated by Django 4.2 on 2023-04-26 20:13

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('competitor', '0012_alter_registration_tire_year'),
        ('financial', '0006_lot_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.IntegerField(choices=[(1, 'Aberto'), (2, 'Concluido'), (3, 'Cancelado')], default=1, verbose_name='Status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financial.lot', verbose_name='Lote')),
                ('registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competitor.registration', verbose_name='Inscrição')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
            },
        ),
        migrations.AddField(
            model_name='paymenthistory',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='financial.order', verbose_name='Criado por'),
        ),
    ]
