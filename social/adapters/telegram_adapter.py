from social.adapters.base_adapter import BaseAdapter

from social.serializers_adapter import TelegramSerializer


class TelegramAdapter(BaseAdapter):
    verbose_name = 'Telegram'
    serializer = TelegramSerializer

    def send_message_to_channel(self, message_text: str, channel: int):
        ...
