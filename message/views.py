import json

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from social.adapters import adapter_name_to_class
from social.models import Social


class MessageView(APIView):
    def get(self, request):
        social = Social.objects.get(pk=2)
        adapter_class = adapter_name_to_class(social.adapter)
        credentials = json.loads(social.credentials)
        adapter = adapter_class(**credentials)
        adapter.send_message_to_channel('Hello world!', 0)

        response_data = {}
        return Response(status=status.HTTP_200_OK, data=response_data)
