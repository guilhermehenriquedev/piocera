# Generated by Django 4.2 on 2023-04-23 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitor', '0010_typecompetitor_alter_competitorsregistration_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typecompetitor',
            name='name',
            field=models.CharField(max_length=150, unique=True, verbose_name='Nome'),
        ),
    ]