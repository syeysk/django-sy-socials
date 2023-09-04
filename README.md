# Шаблон микросервисов

Пожалуйста, используйте данный репозиторий-шаблон для создания новых микросервисов.

## Введение

## Запуск

Скачивание репозитория:

```sh
git clone https://github.com/your_account/your_repo
```

Установка зависимостей:

```sh
pip install -r requirements.txt
```

Применение миграций:

```sh
python manage.py migrate
```

Заполнить переменные окружения, добавив и заполнив файл `.env`

Запуск сервера:

```sh
python manage.py runserver
```

Проверка доступности сервера:

<http://127.0.0.1:8000/intro/>

HTTP/2 200 возвращает JSON ответ.

## API сервера

[Документация API](https://github.com/TVP-Support/django_knowledge/wiki)

## План разработки микросервиса

1. [Основной план](ROADMAP.md)
