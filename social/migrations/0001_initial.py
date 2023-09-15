# Generated by Django 4.2.1 on 2023-09-15 03:00

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
            name='Social',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adapter', models.CharField(choices=[('Telegram', 'Telegram'), ('Discord', 'Discord')], max_length=30, verbose_name='Социальная сеть')),
                ('bot', models.CharField(max_length=30, verbose_name='Бот')),
                ('credentials', models.TextField(max_length=10000, verbose_name='Данные для подключения')),
                ('title', models.CharField(max_length=100, verbose_name='Название подключения')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Подключение к социальным сетям',
                'verbose_name_plural': 'Подключения к социальным сетям',
            },
        ),
    ]
