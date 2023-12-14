# Generated by Django 4.2 on 2023-04-20 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_website_facebook_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='number_of_countries',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Quantidade de países'),
        ),
        migrations.AlterField(
            model_name='website',
            name='number_of_participants',
            field=models.PositiveIntegerField(blank=True, help_text='Colocar apenas número sem o milhar. Ex: 15 se for 15 mil.', null=True, verbose_name='Quantidade de participantes'),
        ),
        migrations.AlterField(
            model_name='website',
            name='number_of_states',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Quantidade de estados'),
        ),
    ]