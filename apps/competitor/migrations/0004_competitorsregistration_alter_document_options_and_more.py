# Generated by Django 4.2 on 2023-04-19 14:40

import competitor.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('competitor', '0003_copilotregistration_registration_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitorsRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_number', models.IntegerField(blank=True, null=True, verbose_name='Número de inscrição')),
                ('number', models.IntegerField(blank=True, null=True, verbose_name='Número')),
                ('thermo', models.BooleanField(default=False, verbose_name='Aceite Termo')),
                ('competitor_card', models.BooleanField(default=False, verbose_name='Geração do cartão do competidor')),
            ],
            options={
                'verbose_name': 'Inscrição do Competidor',
                'verbose_name_plural': 'Inscrições do Competidor',
            },
        ),
        migrations.AlterModelOptions(
            name='document',
            options={'verbose_name': 'Modelo da Documentação', 'verbose_name_plural': 'Modelos das Documentações'},
        ),
        migrations.AlterModelOptions(
            name='registration',
            options={'verbose_name': 'Inscrição', 'verbose_name_plural': 'Inscrições'},
        ),
        migrations.AlterModelOptions(
            name='registrationdocuments',
            options={'verbose_name': 'Documentação da Inscrição', 'verbose_name_plural': 'Documentações da inscrição'},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'verbose_name': 'Equipe', 'verbose_name_plural': 'Equipes'},
        ),
        migrations.RemoveField(
            model_name='registration',
            name='competitor_card',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='driver_number',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='pilot',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='pilot_thermo',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='registration_number',
        ),
        migrations.AlterField(
            model_name='document',
            name='model',
            field=models.FileField(blank=True, null=True, upload_to=competitor.models.get_path_model_documentation),
        ),
        migrations.AlterField(
            model_name='registrationdocuments',
            name='document_file',
            field=models.FileField(upload_to=competitor.models.get_path_documentation),
        ),
        migrations.DeleteModel(
            name='CopilotRegistration',
        ),
        migrations.AddField(
            model_name='competitorsregistration',
            name='registration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competitor.registration', verbose_name='Inscrição'),
        ),
        migrations.AddField(
            model_name='competitorsregistration',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
    ]