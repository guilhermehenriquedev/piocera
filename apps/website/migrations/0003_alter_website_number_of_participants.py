# Generated by Django 4.2 on 2023-04-20 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_alter_questions_options_alter_website_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='number_of_participants',
            field=models.IntegerField(blank=True, help_text='Colocar apenas número sem o milhar. Ex: 15 se for 15 mil.', null=True, verbose_name='Quantidade de participantes'),
        ),
    ]
