# Generated by Django 4.2 on 2023-04-23 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_user_cnh_alter_user_cpf_alter_user_rg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='allergy',
            field=models.ManyToManyField(blank=True, to='users.allergy', verbose_name='Alergia'),
        ),
    ]
