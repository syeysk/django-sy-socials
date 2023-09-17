from rest_framework import serializers


class KnowledgeSearcherTelegramSerializer(serializers.Serializer):
    default_source = serializers.CharField(help_text='База по-умолчанию', required=False, allow_blank=True)
