# Generated by Django 4.2 on 2023-09-04 17:33

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competitor', '0028_boleto_created_at_boleto_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklistitem',
            name='models_url',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='Modelo'),
        ),
    ]
