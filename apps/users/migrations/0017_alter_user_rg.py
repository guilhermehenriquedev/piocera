# Generated by Django 4.2 on 2023-04-29 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_user_organ_expedidor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='rg',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='RG'),
        ),
    ]
