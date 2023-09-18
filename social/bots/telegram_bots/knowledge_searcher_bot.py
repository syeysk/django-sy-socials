from urllib.parse import quote

from rest_framework.response import Response
from rest_framework import status

from django_sy_framework.utils.universal_api import API
from social.adapters import TelegramAdapter

from social.logger import logger
from social.serializers_bot import KnowledgeSearcherTelegramSerializer

DEFAULT_COUNT_ON_PAGE = 10


def note_search(query, search_by='all', operator='or', count_on_page=15, page_number=1, fields='title', source=None):
    params = {
        'count_on_page': count_on_page,
        'fields': fields,
        'operator': operator,
        'page_number': page_number,
        'search-by': search_by,
    }
    if source:
        params['source'] = source

    api = API('1', 'note')
    query = quote(query, safe='')
    response = api.note.search.get(f'/{query}/', params=params)
    if response.status_code != 200:
        return None

    return response.json()


def escape_url_parts(string: str):
    """For parse_mode = MarkdownV2 only"""
    return string.replace(')', '\\)').replace('\\', '\\\\')


def escape_other_parts(string: str):
    """For parse_mode = MarkdownV2 only"""
    for symbol in '_*[]()~`>#+-=|{}.!':
        string = string.replace(symbol, f'\\{symbol}')

    return string


def build_message_body(result_data):
    links = []
    results = result_data['results']
    numeration_from = (result_data['page_number'] - 1) * result_data['count_on_page'] + 1
    for index, result in enumerate(results, numeration_from):
        title = escape_other_parts(result['title'])
        note_url = escape_other_parts(result['url'])
        source = escape_other_parts(quote(result_data['source']))
        links.append(f'{index}\\. [{title}]({note_url}?source={source})')

    links = '\n'.join(links)
    count = result_data['count']
    return f'Найдено результатов: {count}\n\n{links}'


def build_paginator_params(count_pages, page_num=1):
    btn_count_pages = {
        'text': f'{page_num}/{count_pages}',
        'callback_data': 'none',
    }
    btn_prev = {
        'text': '<< prev' if page_num > 1 else ' ',
        'callback_data': f'{page_num - 1}' if page_num > 1 else 'none',
    }
    btn_next = {
        'text': 'next >>' if page_num < count_pages else ' ',
        'callback_data': f'{page_num + 1}' if page_num < count_pages else 'none',
    }
    return {
        'inline_keyboard': [[btn_prev, btn_count_pages, btn_next]]
    }


def build_search_result_message(message, message_text, source):
    if not message_text:
        return {
            'chat_id': message['chat']['id'],
            'text': 'для поиска введите `\\/s фраза для поиска`',
            'reply_to_message_id': message['message_id'],
            'parse_mode': 'MarkdownV2',
        }

    result_data = note_search(message_text, source=source)
    params = {
        'chat_id': message['chat']['id'],
        'text': build_message_body(result_data) if result_data else 'Ошибка сервера',
        'reply_to_message_id': message['message_id'],
        'disable_web_page_preview': True,
        'parse_mode': 'MarkdownV2',
    }
    if result_data:
        params['reply_markup'] = build_paginator_params(result_data['pages'])

    return params


def build_start_message(message, source):
    text = (
        f'Бот поиска по Базе знаний `{source}` микросервиса заметок `cachebrain\\.fun`\n\n'
        'Добавлять заметки может любой зарегистрированный пользователь\\.\n'
        'Микросервис заметок является малой частью большой Платформы межкомандного взаимодействия \\- '
        'экспериментального результата коллективных обсуждений\\.\n\n'
        'Принять участие в обсуждениях можете и Вы, например, написав свои идеи и предложения в чате, '
        'к которому подключён бот\\.\n\n'
        'Спасибо \\:З'
    )
    return {
        'chat_id': message['chat']['id'],
        'text': text,
        'reply_to_message_id': message['message_id'],
        'disable_web_page_preview': True,
        'parse_mode': 'MarkdownV2',
    }


def process_callback(callback_query, source):
    results_message = callback_query['message']
    page_num = int(callback_query['data'])

    query = results_message['reply_to_message']['text']
    if query.startswith('.s '):
        query = query[3:]

    result_data = note_search(query, page_number=page_num, source=source)

    params = {
        'chat_id': results_message.get('chat').get('id'),
        'message_id': results_message.get('message_id'),
        'text': build_message_body(result_data) if result_data else 'Ошибка сервера',
        'disable_web_page_preview': True,
        'parse_mode': 'MarkdownV2',
    }
    if result_data:
        params['reply_markup'] = build_paginator_params(result_data['pages'], page_num)

    return params


class KnowledgeSearcherBot(TelegramAdapter):
    verbose_name = 'Поисковик по базе знаний'
    serializer = KnowledgeSearcherTelegramSerializer
    buttons = TelegramAdapter.buttons + [
        {
            'btn_set_commands': {'verbose_name': 'Установить команды'},
            'btn_get_commands': {'verbose_name': 'Посмотреть команды'},
        },
    ]

    def btn_set_commands(self):
        """

        :param request:
        :return: False if unsuccess, True if success. Or tupple of (True/False, 'message text')
        """
        commands = [
            {'command': 'start', 'description': 'о боте поиска по базе знаний'},
            {'command': 's', 'description': 'ищет в базе знаний'},
        ]
        tg_response = self.set_my_commands({'commands': commands})
        if tg_response.status_code == 200:
            json_data = tg_response.json()
            return json_data['ok'] and json_data['result']

        logger.error(f'unknown answer in set_commands of KnowledgeSearcherBot: {tg_response.content}')

    def btn_get_commands(self):
        tg_response = self.get_my_commands({})
        if tg_response.status_code == 200:
            json_data = tg_response.json()
            if json_data['ok']:
                commands_lines = []
                for command in json_data['result']:
                    commands_lines.append('<b>/{command}</b> - {description}'.format(**command))

                return True, '<br>'.join(commands_lines) if commands_lines else 'Команды не установлены'

        logger.error(f'unknown answer in get_commands of KnowledgeSearcherBot: {tg_response.content}')

    def hook_post_view(self, request):
        source = self.social.bot_settings.get('default_source') or None
        message = request.data.get('message') or request.data.get('channel_post')
        if message:
            command, text_without_command = self.extract_command_from_message(message, True)
            if command == 's':
                params = build_search_result_message(message, text_without_command, source)
                self.send_message(params)
            elif command == 'start':
                params = build_start_message(message, source)
                self.send_message(params)

        callback_query = request.data.get('callback_query')
        if callback_query:
            if callback_query['data'] != 'none':
                params = process_callback(callback_query, source)
                self.edit_message(params)

        if not message and not callback_query:
            logger.error(f'unknown content in hook_post_view of KnowledgeSearcherBot: {request.data}')

        return Response(status=status.HTTP_200_OK)
