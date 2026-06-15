# Чат-бот Telegram на базе YandexGPT для API Bitrix24

Интеллектуальный чат-бот, отвечающий на вопросы разработчиков по документации API Bitrix24.

## Архитектура
Проект модульный:
- `database.py`: Работа с PostgreSQL через SQLAlchemy.
- `scraper.py`: Парсинг документации через Selenium.
- `yandex_assistant.py`: Интеграция с Yandex Assistant (RAG).
- `telegram_bot.py`: Интерфейс взаимодействия с пользователем.

## Описание файла .env
Для работы создайте файл `.env` в корне проекта и заполните его:

| Переменная | Описание | Пример |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Токен бота от @BotFather | `123456:ABCdef...` |
| `POSTGRES_USER` | Пользователь PostgreSQL | `postgres` |
| `POSTGRES_PASSWORD` | Пароль PostgreSQL | `mysecretpassword` |
| `POSTGRES_DB` | Имя базы данных | `bitrix_bot_db` |
| `POSTGRES_HOST` | Хост БД | `localhost` |
| `POSTGRES_PORT` | Порт БД | `5432` |
| `YANDEX_OAUTH_TOKEN` | OAuth-токен Яндекс (для получения IAM) | `y0_AgAAAA...` |
| `YANDEX_FOLDER_ID` | ID каталога в Yandex Cloud | `b1g...` |
| `YANDEX_ASSISTANT_ID` | ID созданного Ассистента | `assistant-...` |
| `SELENIUM_HEADLESS` | Запуск браузера без окна (True/False) | `True` |

## Установка и запуск
1. `pip install -r requirements.txt`
2. Настройте PostgreSQL и создайте БД `bitrix_bot_db`.
3. Заполните `.env`.
4. Запустите парсер для наполнения БД: `python modules/scraper.py`
5. Запустите бота: `python main.py`