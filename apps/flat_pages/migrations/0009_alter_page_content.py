# Generated by Django 4.2 on 2023-07-25 02:22

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('flat_pages', '0008_page_external_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='content',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='Texto'),
        ),
    ]