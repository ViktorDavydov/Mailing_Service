# Generated by Django 4.2.4 on 2023-12-27 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0025_alter_logs_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='logs',
            name='send_name',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='mailer.sendoptions', verbose_name='название рассылки'),
        ),
    ]