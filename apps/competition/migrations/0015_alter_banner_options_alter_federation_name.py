# Generated by Django 4.2 on 2023-04-23 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0014_remove_categorymodality_modality_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banner',
            options={'verbose_name': 'Banner e background', 'verbose_name_plural': 'Banners e backgrounds'},
        ),
        migrations.AlterField(
            model_name='federation',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Nome'),
        ),
    ]