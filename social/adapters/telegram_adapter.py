import requests

from social.adapters.base_adapter import BaseAdapter
from social.serializers_adapter import TelegramSerializer


class TelegramAdapter(BaseAdapter):
    verbose_name = 'Telegram'
    serializer = TelegramSerializer
    url_template = 'https://api.telegram.org/bot{}'

    def __init__(self, token):
        self.url = self.url_template.format(token)

    def send_message_to_channel(self, text: str, channel: int):
        params = {
            'chat_id': channel,
            'text': text,
            # 'reply_to_message_id': message_id,
            'disable_web_page_preview': True,
            'parse_mode': 'Markdown',
            # 'reply_markup': reply_markup,
        }
        requests.post(f'{self.url}/sendMessage', json=params)
