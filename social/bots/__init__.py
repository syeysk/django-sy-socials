from social.adapters import adapter_name_to_class
from social.bots import telegram_bots


def bot_name_to_class(adapter_name, bot_name):
    package_of_bots = globals()['{}_bots'.format(adapter_name.lower())]
    return getattr(package_of_bots, f'{bot_name}Bot')


def get_bot_names(adapter_name, add_class=False):
    adapter_class = adapter_name_to_class(adapter_name)
    bot_names = []
    for subclass in adapter_class.__subclasses__():
        bot_names.append(
            (subclass.__name__[:-3], subclass if add_class else subclass.verbose_name),
        )

    return bot_names
