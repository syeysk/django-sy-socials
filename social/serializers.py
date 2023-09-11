import json

from rest_framework import serializers

from social.models import Social


class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = ['title', 'adapter', 'credentials']

    def validate(self, data):
        from social.adapters import adapter_name_to_class

        uploader_class = adapter_name_to_class(data['adapter'])
        if hasattr(uploader_class, 'serializer'):
            serializer = uploader_class.serializer(data=json.loads(data['credentials']))
            serializer.is_valid(raise_exception=False)
            if serializer.errors:
                raise serializers.ValidationError({'credentials': serializer.errors})

        return data
