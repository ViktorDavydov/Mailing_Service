# Generated by Django 5.0 on 2023-12-10 14:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0004_sendoptions_send_name_alter_client_client_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='send_options_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mailer.sendoptions', verbose_name='наименование рассылки'),
        ),
    ]
