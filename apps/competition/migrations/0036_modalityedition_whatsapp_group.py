# Generated by Django 4.2 on 2023-08-01 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0035_edition_check_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='modalityedition',
            name='whatsapp_group',
            field=models.CharField(blank=True, max_length=500, verbose_name='Link do grupo do whatsapp'),
        ),
    ]
