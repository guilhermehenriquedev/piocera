# Generated by Django 4.2 on 2023-08-01 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_newsletter'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='interest_area',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Área de Interesse'),
        ),
    ]
