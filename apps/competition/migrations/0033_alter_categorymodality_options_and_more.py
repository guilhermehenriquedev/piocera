# Generated by Django 4.2 on 2023-05-08 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0032_alter_competitioncategory_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categorymodality',
            options={'ordering': ('order',), 'verbose_name': 'Categoria da Modalidade', 'verbose_name_plural': 'Categorias das Modalidades'},
        ),
        migrations.AlterModelOptions(
            name='competitioncategory',
            options={'verbose_name': 'Categoria', 'verbose_name_plural': 'Categorias'},
        ),
        migrations.RemoveField(
            model_name='competitioncategory',
            name='order',
        ),
        migrations.AddField(
            model_name='categorymodality',
            name='order',
            field=models.IntegerField(blank='True', null='True', verbose_name='Ordem'),
            preserve_default='True',
        ),
    ]
