# Generated by Django 4.2 on 2023-07-20 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_alter_champion_sponsorship_alter_champion_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='champion',
            name='sponsorship',
            field=models.CharField(max_length=500, null=True, verbose_name='Sponsorship'),
        ),
    ]
