import uuid

import requests

from social.adapters.base_adapter import BaseAdapter
from social.logger import logger
from social.serializers_adapter import TelegramSerializer


class TelegramAdapter(BaseAdapter):
    """Telegram's API documentation: https://core.telegram.org/bots/api/"""
    verbose_name = 'Telegram'
    serializer = TelegramSerializer
    url_template = 'https://api.telegram.org/bot{}'

    def __init__(self, *args, token):
        super().__init__(*args)
        self.url = self.url_template.format(token)

    def send_message_to_channel(self, text: str, channel: int):
        params = {
            'chat_id': channel,
            'text': text,
            'disable_web_page_preview': True,
            'parse_mode': 'Markdown',
        }
        requests.post(f'{self.url}/sendMessage', json=params)

    def verify_hook(self, request):
        return request.META.get('HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN') == self.social.any_data.get('secret_token')

    def set_hook(self, url):
        secret_token = str(uuid.uuid4())
        self.social.any_data['secret_token'] = secret_token
        response = requests.post(f'{self.url}/setWebhook', json={'url': url, 'secret_token': secret_token})
        if response.status_code == 200:
            response_json = response.json()
            if response_json['ok']:
                self.social.save()
                return True

    def get_hook(self):
        response = requests.post(f'{self.url}/getWebhookInfo')
        if response.status_code == 200:
            response_json = response.json()
            if response_json['ok']:
                return response_json['result']['url']

    def delete_hook(self):
        ...

    def send_message(self, params):
        response = requests.post(f'{self.url}/sendMessage', json=params)
        if response.status_code != 200:
            logger.log(f'Error during sending message: {response.content}\n\n')

    def edit_message(self, params):
        response = requests.post(f'{self.url}/editMessageText', json=params)
        if response.status_code != 200:
            logger.log(f'Error during editing message: {response.content}\n\n')
