# Generated by Django 4.2 on 2023-07-06 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('competitor', '0023_document_slug_alter_document_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Nome')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Data de atualização')),
            ],
            options={
                'verbose_name': 'Checklist',
                'verbose_name_plural': 'Checklists',
            },
        ),
        migrations.CreateModel(
            name='CompetitorCheckList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competitor.checklist', verbose_name='Checklist')),
                ('competitor_registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competitor.competitorsregistration', verbose_name='Inscrição do Competidor')),
            ],
            options={
                'verbose_name': 'Checklist do Competidor',
                'verbose_name_plural': 'Checklists dos Competidores',
            },
        ),
        migrations.CreateModel(
            name='CheckListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500, verbose_name='Texto')),
                ('valid', models.BooleanField(default=False, verbose_name='Confirmado')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Data de atualização')),
                ('checklist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competitor.checklist', verbose_name='Checklist')),
            ],
            options={
                'verbose_name': 'Checklist Item',
                'verbose_name_plural': 'Checklists Items',
            },
        ),
    ]
