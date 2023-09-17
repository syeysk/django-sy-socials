from rest_framework import serializers


class KnowledgeSearcherTelegramSerializer(serializers.Serializer):
    default_source = serializers.CharField(help_text='База по-умолчанию', is_required=False)
