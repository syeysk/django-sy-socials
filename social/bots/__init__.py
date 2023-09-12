from social.bots import telegram_bots


def snake2camel(snake_case):
    return ''.join(word.title() for word in snake_case.split('_'))


def bot_name_to_class(adapter_name, bot_name):
    package_of_bots = globals()['{}_bots'.format(adapter_name.lower())]
    bot_module = getattr(package_of_bots, bot_name)
    return getattr(bot_module, snake2camel(bot_name))
