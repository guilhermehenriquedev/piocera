# Generated by Django 4.2 on 2023-04-23 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_remove_user_allergy_user_allergy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cnh',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True, verbose_name='CNH'),
        ),
        migrations.AlterField(
            model_name='user',
            name='cpf',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='user',
            name='rg',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='RG'),
        ),
    ]
