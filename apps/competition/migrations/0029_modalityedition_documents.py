# Generated by Django 4.2 on 2023-05-06 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitor', '0016_alter_registration_registration_number'),
        ('competition', '0028_alter_sponsor_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='modalityedition',
            name='documents',
            field=models.ManyToManyField(to='competitor.document', verbose_name='Documentos'),
        ),
    ]