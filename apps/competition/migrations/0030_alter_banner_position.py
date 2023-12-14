# Generated by Django 4.2 on 2023-05-06 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0029_modalityedition_documents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='position',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'BANNER PRICIPAL (1741x743)'), (2, 'BANNER TEXTO (1440x121)'), (3, 'BANNER OPÇÕES DE ESPORTES (4 banners - 288x124)'), (4, 'BACKGROUND DADOS'), (5, 'BACKGROUND EXPERIÊNCIA (1443x1140)'), (6, 'BACKGROUND AÇÕES (1443x1140)'), (7, 'BACKGROUND PERGUNTAS (1443x1140)'), (8, 'AREA COMPETIDOR (261 x 1077)')], null=True, verbose_name='Posição'),
        ),
    ]