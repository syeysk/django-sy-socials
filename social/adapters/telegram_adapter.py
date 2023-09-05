from social.adapters.base_adapter import BaseAdapter


class TelegramAdapter(BaseAdapter):
    verbose_name = 'Telegram'
    def send_message_to_channel(self, message_text: str, channel: int):
        ...
