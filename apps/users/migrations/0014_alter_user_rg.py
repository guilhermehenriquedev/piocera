# Generated by Django 4.2 on 2023-04-28 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_user_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='rg',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='RG'),
        ),
    ]
