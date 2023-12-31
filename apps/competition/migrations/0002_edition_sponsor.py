# Generated by Django 4.2 on 2023-04-19 04:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Edition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano', models.CharField(max_length=4, verbose_name='Ano')),
                ('type', models.CharField(choices=[('1', 'CERAPIO'), ('2', 'PIOCERA')], default='1', max_length=2, verbose_name='Tipo')),
                ('edition_date', models.DateField(verbose_name='Data da edição')),
                ('registration_start_date', models.DateField(verbose_name='Data início para inscrição')),
                ('registration_end_date', models.DateField(verbose_name='Data final para inscrição')),
                ('about', models.TextField(verbose_name='Sobre')),
                ('status', models.CharField(choices=[('1', 'RASCUNHO'), ('3', 'ATIVADA'), ('2', 'DESATIVADA')], default=1, max_length=2, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Patrocinador')),
                ('type', models.CharField(blank=True, choices=[('1', 'PATROCINADOR'), ('2', 'CO-PATROCINADOR'), ('3', 'APOIO')], max_length=2, null=True, verbose_name='Tipo')),
                ('logo', models.ImageField(upload_to=None)),
                ('banner', models.ImageField(upload_to=None)),
                ('edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.edition', verbose_name='Edição')),
            ],
        ),
    ]
