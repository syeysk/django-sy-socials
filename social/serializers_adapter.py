from rest_framework import serializers


class TelegramSerializer(serializers.Serializer):
    token = serializers.CharField(help_text='Telegram-токен')
