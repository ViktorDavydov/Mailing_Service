# Generated by Django 4.2.4 on 2023-12-27 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_user_verification_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verification_code',
            field=models.CharField(blank=True, default='70586513', max_length=8, null=True, verbose_name='код подтверждения почты'),
        ),
    ]
