# Generated by Django 4.2 on 2023-05-06 03:00

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flat_pages', '0005_pagefiles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Texto'),
        ),
    ]
