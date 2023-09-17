import json

from rest_framework import serializers

from social.models import Social


class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = ['title', 'adapter', 'credentials', 'bot', 'bot_settings']

    def validate(self, data):
        from social.adapters import adapter_name_to_class
        from social.bots import bot_name_to_class

        adapter_class = adapter_name_to_class(data['adapter'])
        if hasattr(adapter_class, 'serializer'):
            serializer = adapter_class.serializer(data=json.loads(data['credentials']))
            serializer.is_valid(raise_exception=False)
            if serializer.errors:
                raise serializers.ValidationError({'credentials': serializer.errors})

        bot_class = bot_name_to_class(data['adapter'], data['bot'])
        if hasattr(bot_class, 'serializer'):
            serializer = bot_class.serializer(data=data['bot_settings'])
            serializer.is_valid(raise_exception=False)
            if serializer.errors:
                raise serializers.ValidationError({'bot_settings': serializer.errors})

        return data
