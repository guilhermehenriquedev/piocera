# Generated by Django 4.2 on 2023-04-21 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('image_bank', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photos',
            name='album',
        ),
        migrations.AddField(
            model_name='album',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='Data'),
        ),
        migrations.CreateModel(
            name='SubAlbum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nome')),
                ('status', models.PositiveIntegerField(choices=[(1, 'RASCUNHO'), (3, 'ATIVADA'), (2, 'DESATIVADA')], default=1, verbose_name='Status')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='image_bank.album', verbose_name='Album')),
            ],
            options={
                'verbose_name': 'Sub album',
                'verbose_name_plural': 'Sub Albuns',
            },
        ),
        migrations.AddField(
            model_name='photos',
            name='subalbum',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='image_bank.subalbum', verbose_name='Sub Album'),
        ),
    ]
