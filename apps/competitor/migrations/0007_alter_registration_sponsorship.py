# Generated by Django 4.2 on 2023-04-23 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitor', '0006_competitorsregistration_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='sponsorship',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Patrocinador'),
        ),
    ]
