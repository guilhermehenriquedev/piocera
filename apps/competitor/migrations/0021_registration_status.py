# Generated by Django 4.2 on 2023-05-08 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitor', '0020_registrationdocuments_approval_status_changed'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='status',
            field=models.CharField(choices=[('1', 'Registro'), ('2', 'Pago'), ('3', 'Homologado'), ('4', 'Cancelado')], default='1', max_length=12, verbose_name='status'),
        ),
    ]
