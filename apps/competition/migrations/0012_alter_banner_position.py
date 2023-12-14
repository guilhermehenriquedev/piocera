# Generated by Django 4.2 on 2023-04-20 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0011_alter_banner_position_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='position',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'BANNER PRICIPAL (1741x743)'), (2, 'BANNER TEXTO (1440x121)'), (3, 'BANNER OPÇÕES DE ESPORTES (4 banners - 288x124)'), (4, 'BACKGROUND DADOS'), (5, 'BACKGROUND EXPERIÊNCIA (1443x1140)'), (6, 'BACKGROUND AÇÕES (1443x1140)'), (7, 'BACKGROUND PERGUNTAS (1443x1140)')], null=True, verbose_name='Posição'),
        ),
    ]