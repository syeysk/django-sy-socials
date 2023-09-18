from rest_framework import serializers


class KnowledgeSearcherTelegramSerializer(serializers.Serializer):
    default_source = serializers.CharField(help_text='База знаний по-умолчанию', required=False, allow_blank=True)


class InformPagesTelegramSerializer(serializers.Serializer):
    source = serializers.CharField(help_text='База знаний, содержащая страницы', required=True, allow_blank=False)
