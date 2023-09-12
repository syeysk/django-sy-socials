from urllib.parse import quote

import requests
from rest_framework.response import Response
from rest_framework import status

from django_sy_framework.utils.universal_api import API
from social.adapters import TelegramAdapter

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
    response = api.note.search.get(f'/{query}', params=params)
    if response.status_code != 200:
        raise Exception(f'status code is {response.status_code} {response.content}')

    return response.json()


def build_message_body(result_data):
    links = []
    results = result_data['results']
    numeration_from = (result_data['page_number'] - 1) * result_data['count_on_page'] + 1
    for index, result in enumerate(results, numeration_from):
        title = result['title']
        quoted_title = quote(title)
        note_url = result['url']
        links.append(f'{index}. [{title}]({note_url}db/{quoted_title}.md)')

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


def process_message(message, is_from_chat, url):
    message_text = message.get('text', '')
    if is_from_chat and message_text.startswith('.s '):
        message_text = message_text[3:]

    if message_text:
        result_data = note_search(message_text)
        params = {
            'chat_id': message['chat']['id'],
            'text': build_message_body(result_data),
            'reply_to_message_id': message['message_id'],
            'disable_web_page_preview': True,
            'parse_mode': 'Markdown',
            'reply_markup': build_paginator_params(result_data['pages']),
        }
        requests.post(f'{url}/sendMessage', json=params)


def process_callback(callback_query, url):
    results_message = callback_query['message']
    page_num = int(callback_query['data'])

    query = results_message['reply_to_message']['text']
    if query.startswith('.s '):
        query = query[3:]

    result_data = note_search(query, page_number=page_num)

    reply_markup = build_paginator_params(result_data['pages'], page_num)
    params = {
        'chat_id': results_message.get('chat').get('id'),
        'message_id': results_message.get('message_id'),
        'text': build_message_body(result_data),
        'disable_web_page_preview': True,
        'parse_mode': 'Markdown',
        'reply_markup': reply_markup,
    }
    requests.post(f'{url}/editMessageText', json=params)


class KnowledgeSearcherBot(TelegramAdapter):
    def hook_view(self, request):
        message = request.data.get('message') or request.data.get('channel_post')
        if message:
            process_message(message, 'channel_post' in request.data, self.url)

        callback_query = request.data.get('callback_query')
        if callback_query:
            if callback_query['data'] == 'none':
                return Response(status=status.HTTP_200_OK, data={})

            process_callback(callback_query, self.url)

        return Response(status=status.HTTP_200_OK, data={})