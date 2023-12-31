# Generated by Django 4.2 on 2023-05-06 02:47

from django.db import migrations, models
import django.db.models.deletion
import flat_pages.models


class Migration(migrations.Migration):

    dependencies = [
        ('flat_pages', '0004_categorypage_created_at_categorypage_updated_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nome do arquivo')),
                ('description', models.CharField(max_length=255, verbose_name='Descrição do arquivo')),
                ('file', models.FileField(upload_to=flat_pages.models.get_path_archive_page, verbose_name='Arquivo')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flat_pages.page', verbose_name='Página')),
            ],
            options={
                'verbose_name': 'Arquivos da Página',
                'verbose_name_plural': 'Arquivos da Páginas',
            },
        ),
    ]
