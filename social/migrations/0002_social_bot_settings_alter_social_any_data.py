# Generated by Django 4.2.1 on 2023-09-17 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='social',
            name='bot_settings',
            field=models.JSONField(default=dict, verbose_name='Настройки бота'),
        ),
        migrations.AlterField(
            model_name='social',
            name='any_data',
            field=models.JSONField(default=dict, verbose_name='Произвольные данные'),
        ),
    ]
