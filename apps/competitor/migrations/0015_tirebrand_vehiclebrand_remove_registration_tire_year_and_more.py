# Generated by Django 4.2 on 2023-05-05 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('competitor', '0014_competitorsregistration_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TireBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Marca de pneu',
                'verbose_name_plural': 'Marcas de pneus',
            },
        ),
        migrations.CreateModel(
            name='VehicleBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Marca de veículo',
                'verbose_name_plural': 'Marcas de veículos',
            },
        ),
        migrations.RemoveField(
            model_name='registration',
            name='tire_year',
        ),
        migrations.AddField(
            model_name='registration',
            name='wheel_rim',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Aro da roda'),
        ),
        migrations.CreateModel(
            name='VehicleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nome')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competitor.vehiclebrand', verbose_name='Marca')),
            ],
            options={
                'verbose_name': 'Modelo de veículo',
                'verbose_name_plural': 'Modelos de veículos',
            },
        ),
        migrations.AlterField(
            model_name='registration',
            name='tire_brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='competitor.tirebrand', verbose_name='Marca do pneu'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='vehicle_brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='competitor.vehiclebrand', verbose_name='Marca do veículo'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='vehicle_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='competitor.vehiclemodel', verbose_name='Modelo do veículo'),
        ),
    ]
