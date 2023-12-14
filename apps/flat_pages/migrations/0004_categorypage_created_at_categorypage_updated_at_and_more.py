# Generated by Django 4.2 on 2023-05-04 13:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('flat_pages', '0003_page_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorypage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Data de criação'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='categorypage',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Data de atualização'),
        ),
        migrations.AddField(
            model_name='page',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Data de criação'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='page',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Data de atualização'),
        ),
    ]
