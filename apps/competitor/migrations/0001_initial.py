# Generated by Django 4.2 on 2023-04-19 06:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CopilotRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('copilot_number', models.IntegerField(blank=True, null=True, verbose_name='Número do co-piloto')),
                ('copilot_thermo', models.BooleanField(default=False, verbose_name='Termo co-piloto')),
                ('competitor_card', models.BooleanField(default=False, verbose_name='Geração do cartão do competidor')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Título')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('model', models.FileField(blank=True, null=True, upload_to='uploads/')),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_number', models.IntegerField(blank=True, null=True, verbose_name='Número de inscrição')),
                ('has_team', models.BooleanField(default=False, verbose_name='Sem equipe')),
                ('sponsorship', models.TextField(blank=True, null=True, verbose_name='Patrocinador')),
                ('vehicle_brand', models.CharField(blank=True, max_length=150, null=True, verbose_name='Marca do veículo')),
                ('vehicle_model', models.CharField(blank=True, max_length=150, null=True, verbose_name='Modelo do veículo')),
                ('tire_brand', models.CharField(blank=True, max_length=150, null=True, verbose_name='Marca do pneu')),
                ('tire_year', models.CharField(blank=True, max_length=5, null=True, verbose_name='Ano do pneu')),
                ('driver_number', models.IntegerField(blank=True, null=True, verbose_name='Número do piloto')),
                ('pilot_thermo', models.BooleanField(default=False, verbose_name='Termo piloto')),
                ('payment_status', models.BooleanField(default=False, verbose_name='Status de pagamento')),
                ('competitor_card', models.BooleanField(default=False, verbose_name='Geração do cartão do competidor')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nome')),
                ('coordinator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Coordenador')),
            ],
        ),
        migrations.CreateModel(
            name='RegistrationDocuments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_file', models.FileField(upload_to='uploads/')),
                ('approval_status', models.CharField(choices=[('1', 'Inscrição'), ('2', 'Em análise'), ('3', 'Aprovado'), ('4', 'Negado'), ('5', 'Cancelado')], default=1, max_length=2, verbose_name='Status de aprovação')),
                ('document_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competitor.document', verbose_name='Tipo de documento')),
                ('registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competitor.registration', verbose_name='Inscrição')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
        ),
    ]