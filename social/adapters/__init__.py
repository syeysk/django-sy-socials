from social.adapters.base_adapter import BaseAdapter
from social.adapters.telegram_adapter import TelegramAdapter


def get_adapter_names(add_class=False):
    service_names = []
    for subclass in BaseAdapter.__subclasses__():
        service_names.append(
            (subclass.__name__[:-7], subclass if add_class else subclass.verbose_name),
        )

    return service_names
