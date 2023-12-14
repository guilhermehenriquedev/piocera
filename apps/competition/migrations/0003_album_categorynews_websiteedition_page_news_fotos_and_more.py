# Generated by Django 4.2 on 2023-04-19 05:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('competition', '0002_edition_sponsor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nome')),
                ('status', models.CharField(choices=[('1', 'RASCUNHO'), ('3', 'ATIVADA'), ('2', 'DESATIVADA')], default='1', max_length=2, verbose_name='Status')),
                ('edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.edition', verbose_name='Edição')),
            ],
        ),
        migrations.CreateModel(
            name='CategoryNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nome')),
            ],
        ),
        migrations.CreateModel(
            name='WebSiteEdition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_participants_previous_year', models.IntegerField(blank=True, null=True, verbose_name='Quantidade de participantes no ano anterior')),
                ('number_km_previous_year', models.IntegerField(blank=True, null=True, verbose_name='Quantidade de km ano anterior')),
                ('number_days_previous_year', models.IntegerField(blank=True, null=True, verbose_name='Quantidade de dias no ano anterior')),
                ('edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.edition', verbose_name='Edição')),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Título')),
                ('menu_category', models.CharField(choices=[('1', 'O EVENTO'), ('2', 'NOTICIAS'), ('3', 'AGENCIA DE VIAGENS'), ('4', 'CONTATO')], default='1', max_length=2, verbose_name='Categoria do menu')),
                ('content', models.TextField(verbose_name='Conteudo')),
                ('status', models.CharField(choices=[('1', 'RASCUNHO'), ('3', 'ATIVADA'), ('2', 'DESATIVADA')], default='1', max_length=2, verbose_name='Status')),
                ('edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.edition', verbose_name='Edição')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Título')),
                ('cover', models.ImageField(blank=True, null=True, upload_to=None)),
                ('content', models.TextField(blank=True, null=True, verbose_name='Conteúdo')),
                ('publication_date', models.DateTimeField(blank=True, null=True, verbose_name='Data de publicação')),
                ('status', models.CharField(choices=[('1', 'RASCUNHO'), ('3', 'ATIVADA'), ('2', 'DESATIVADA')], default='1', max_length=2, verbose_name='Status')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='competition.categorynews', verbose_name='Categoria')),
                ('edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.edition', verbose_name='Edição')),
            ],
        ),
        migrations.CreateModel(
            name='Fotos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nome')),
                ('foto', models.ImageField(upload_to=None)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.album', verbose_name='Album')),
            ],
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, choices=[('1', 'BANNER PRICIPAL'), ('2', 'BACKGROUND DADOS'), ('3', 'BACKGROUND EXPERIÊNCIA'), ('4', 'BACKGROUND AÇÕES'), ('5', 'BACKGROUND PERGUNTAS')], max_length=2, null=True, verbose_name='Posicao')),
                ('banner', models.ImageField(upload_to=None)),
                ('edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.edition', verbose_name='Edição')),
            ],
        ),
    ]