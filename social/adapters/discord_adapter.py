from social.adapters.base_adapter import BaseAdapter


class DiscordAdapter(BaseAdapter):
    verbose_name = 'Discord'

    def send_message_to_channel(self, text: str, channel: int):
        ...
