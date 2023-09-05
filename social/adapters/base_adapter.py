from typing import Any


class BaseAdapter:
    def send_message_to_channel(self, message_text: str, channel: Any):
        """Send text message into channel. Raise exception if any error"""
        raise NotImplemented()
