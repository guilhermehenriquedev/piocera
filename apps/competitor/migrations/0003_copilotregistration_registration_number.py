# Generated by Django 4.2 on 2023-04-19 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitor', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='copilotregistration',
            name='registration_number',
            field=models.IntegerField(blank=True, null=True, verbose_name='Número de inscrição'),
        ),
    ]
