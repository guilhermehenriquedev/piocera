# Generated by Django 4.2 on 2023-07-06 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('competitor', '0026_alter_competitorchecklist_check_list_item_concluded'),
        ('competition', '0034_competitionmodality_is_apoio_zequinha'),
    ]

    operations = [
        migrations.AddField(
            model_name='edition',
            name='check_list',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='competitor.checklist', verbose_name='Check List'),
        ),
    ]