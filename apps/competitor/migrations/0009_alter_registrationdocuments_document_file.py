# Generated by Django 4.2 on 2023-04-23 02:11

import competitor.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitor', '0008_alter_document_model_alter_document_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationdocuments',
            name='document_file',
            field=models.FileField(upload_to=competitor.models.get_path_documentation, verbose_name='Documentação'),
        ),
    ]