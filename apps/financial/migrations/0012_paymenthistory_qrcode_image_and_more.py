# Generated by Django 4.2 on 2023-05-03 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0011_alter_accountbank_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenthistory',
            name='qrcode_image',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='paymenthistory',
            name='qrcode_key',
            field=models.TextField(null=True),
        ),
    ]
