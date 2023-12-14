# Generated by Django 4.2 on 2023-04-23 13:33

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flat_pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorypage',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=1, editable=False, max_length=150, populate_from='name', unique=True, verbose_name='Link'),
        ),
    ]
