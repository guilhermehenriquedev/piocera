# Generated by Django 4.2 on 2023-04-28 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_user_rg'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='organ_expedidor',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Orgão expedidor'),
        ),
    ]
