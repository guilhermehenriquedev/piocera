# Generated by Django 4.2 on 2023-04-28 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_user_organ_expedidor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='organ_expedidor',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Orgão Emissor'),
        ),
    ]
