# Generated by Django 4.2 on 2023-04-23 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_allergy_options_alter_user_profile_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='emergency_phone',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Número de contato emergencial'),
        ),
    ]
