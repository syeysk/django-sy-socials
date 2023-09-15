from social.adapters.base_adapter import BaseAdapter
from social.adapters.telegram_adapter import TelegramAdapter
from social.adapters.discord_adapter import DiscordAdapter


def adapter_name_to_class(adapter_name):
    return globals()[f'{adapter_name}Adapter']


def get_adapter_names(add_class=False):
    adapter_names = []
    for subclass in BaseAdapter.__subclasses__():
        adapter_names.append(
            [subclass.__name__[:-7], subclass if add_class else subclass.verbose_name],
        )

    return adapter_names


def get_adapters_properties():
    adapters_properties = {}
    for subclass in BaseAdapter.__subclasses__():
        adapters_properties[subclass.__name__[:-7]] = {
            'verbose_name': subclass.verbose_name,
            'has_hook_buttons': {
                'set': hasattr(subclass, 'set_hook'),
                'get': hasattr(subclass, 'get_hook'),
                'delete': hasattr(subclass, 'delete_hook'),
            },
        }

    return adapters_properties
