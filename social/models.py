from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import resolve_url

from social.adapters import get_adapter_names


class Social(models.Model):
    CHOICES_ADAPTERS = get_adapter_names()
    adapter = models.CharField(verbose_name='Социальная сеть', max_length=30, choices=CHOICES_ADAPTERS, blank=False)
    bot = models.CharField(verbose_name='Бот', max_length=30, blank=False)
    credentials = models.TextField(verbose_name='Данные для подключения', max_length=10000)
    created_by = models.ForeignKey(get_user_model(), null=False, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Название подключения', max_length=100)
    any_data = models.JSONField(verbose_name='Произвольные данные', default=dict)
    bot_settings = models.JSONField(verbose_name='Настройки бота', default=dict)

    @property
    def hook_url(self):
        return '{}{}'.format(settings.SITE_URL, resolve_url('hook', pk=self.pk))

    class Meta:
        verbose_name = 'Подключение к социальным сетям'
        verbose_name_plural = 'Подключения к социальным сетям'
