from rest_framework.response import Response
from rest_framework import status

from social.adapters import TelegramAdapter
from social.serializers_bot import InformPagesTelegramSerializer


class InformPagesBot(TelegramAdapter):
    verbose_name = 'Информационные страницы'
    serializer = InformPagesTelegramSerializer

    def hook_post_view(self, request):
        return Response(status=status.HTTP_200_OK, data={})
