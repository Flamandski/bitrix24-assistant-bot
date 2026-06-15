# 🤖 Telegram-бот помощник по API Bitrix24 на базе YandexGPT

Интеллектуальный чат-бот для разработчиков, отвечающий на вопросы по официальной документации REST API Bitrix24. Использует LLM **YandexGPT** и технологию **RAG (Retrieval-Augmented Generation)** для поиска точных ответов в актуальной базе знаний.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)
![YandexGPT](https://img.shields.io/badge/YandexGPT-5-red?logo=yandex)

## ✨ Возможности

- 💬 Отвечает на вопросы по API Bitrix24 на естественном языке
- 📚 Использует актуальную документацию с `apidocs.bitrix24.ru` в качестве базы знаний
- 🧠 Обработка запросов через YandexGPT 5 (Foundation Models API)
- 🕷️ Автоматический парсинг документации через Selenium
- 🗄️ Хранение данных в PostgreSQL через SQLAlchemy ORM
- 📊 Ведение истории взаимодействий с пользователями
- 🔒 Безопасное хранение секретов через `.env`

## 🛠️ Технологический стек

| Технология | Версия | Назначение |
|---|---|---|
| **Python** | **3.13** | Основной язык разработки |
| python-telegram-bot | 21.9 | Интеграция с Telegram Bot API |
| SQLAlchemy | ≥2.0.35 | ORM для работы с PostgreSQL |
| psycopg[binary] | 3.x | Драйвер PostgreSQL |
| python-dotenv | 1.0.1 | Загрузка переменных окружения |
| Selenium | 4.18.1 | Парсинг динамических веб-страниц |
| requests | 2.31.0 | HTTP-запросы к YandexGPT API |
| PostgreSQL | 16 | Реляционная база данных |
| YandexGPT | latest | LLM для генерации ответов |

> ⚠️ **Важно:** Проект протестирован на **Python 3.13**. Использование Python 3.14 или ниже 3.12 может вызвать проблемы совместимости с библиотеками SQLAlchemy и psycopg.

## 📁 Структура проекта

```
bitrix24-assistant-bot/
│
├── .env                    # Секретные данные (НЕ загружается в git)
├── .gitignore              # Исключения для git
├── requirements.txt        # Зависимости Python
├── README.md               # Документация проекта
├── config.py               # Загрузка переменных окружения
├── main.py                 # Точка входа (оркестратор)
├── create_tables.py        # Скрипт инициализации БД
│
└── modules/
    ├── __init__.py
    ├── database.py         # Модуль БД (SQLAlchemy, модели, CRUD)
    ├── scraper.py          # Модуль парсинга (Selenium)
    ├── yandex_assistant.py # Модуль интеграции с YandexGPT
    └── telegram_bot.py     # Модуль интеграции с Telegram
```

## 💻 Системные требования

- **Python 3.13** (рекомендуется)
- **PostgreSQL 16** (или новее)
- **Google Chrome** (для работы Selenium)
- **Учётная запись Yandex Cloud** с доступом к YandexGPT API
- **Telegram-бот**, созданный через [@BotFather](https://t.me/BotFather)

## 🚀 Установка и запуск

### Шаг 1: Клонирование репозитория

```bash
git clone https://github.com/Flamandski/bitrix24-assistant-bot.git
cd bitrix24-assistant-bot
```

### Шаг 2: Создание виртуального окружения (venv)

Создайте изолированное Python-окружение для проекта:

**Windows (PowerShell):**
```powershell
# Создаём виртуальное окружение на базе Python 3.13
py -3.13 -m venv venv

# Активируем окружение
venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
py -3.13 -m venv venv
venv\Scripts\activate.bat
```

**Linux / macOS:**
```bash
python3.13 -m venv venv
source venv/bin/activate
```

> 💡 После активации в начале строки терминала появится префикс `(venv)`.

### Шаг 3: Установка зависимостей

```bash
# Обновляем pip
python -m pip install --upgrade pip

# Устанавливаем все зависимости из requirements.txt
pip install -r requirements.txt
```

### Шаг 4: Установка и настройка PostgreSQL

1. Скачайте PostgreSQL с официального сайта: https://www.postgresql.org/download/windows/
2. При установке задайте пароль для пользователя `postgres` (запомните его!)
3. Откройте **pgAdmin 4** (устанавливается вместе с PostgreSQL)
4. Создайте новую базу данных:
   - Правой кнопкой по **Databases** → **Create** → **Database...**
   - Имя: `bitrix_bot_db`
   - Owner: `postgres`
   - Нажмите **Save**

### Шаг 5: Получение токенов и ID

#### Telegram Bot Token
1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте `/newbot`, следуйте инструкциям
3. Скопируйте полученный токен

#### Yandex Cloud IAM Token
1. Получите OAuth-токен: https://oauth.yandex.ru/authorize?response_type=token&client_id=1a6990aa636648e9b2ef855fa7bec2fb
2. Обменяйте его на IAM-токен (живёт 12 часов):
   ```bash
   curl -X POST https://iam.api.cloud.yandex.net/iam/v1/tokens \
        -d '{"yandexPassportOauthToken":"ВАШ_OAUTH_TOKEN"}'
   ```
3. Скопируйте значение `iamToken` из ответа
4. В консоли Yandex Cloud (https://console.cloud.yandex.ru/) найдите **Folder ID** (начинается на `b1g`)

### Шаг 6: Создание файла `.env`

В корне проекта создайте файл `.env` и заполните его по шаблону ниже.

### Шаг 7: Инициализация базы данных

```bash
python create_tables.py
```

Этот скрипт создаст в PostgreSQL три таблицы: `users`, `message_history`, `bitrix_docs`.

### Шаг 8: Парсинг документации

Наполните базу знаний документацией с сайта Bitrix24:

```bash
python -m modules.scraper
```

После выполнения в таблице `bitrix_docs` появятся статьи с документацией.

### Шаг 9: Запуск бота

```bash
python main.py
```

Ожидаемый вывод:
```
✅ Переменные окружения загружены из .env
✅ YandexGPT инициализирован (прямой режим)
🚀 Запуск Bitrix24 Assistant Bot...
✅ База данных инициализирована.
🤖 Бот запущен (системные прокси отключены) и ожидает сообщений...
```

## 🔐 Описание файла `.env`

Для работы проекта необходимо создать файл `.env` в корне проекта и заполнить его следующими переменными:

| Переменная | Описание | Пример |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Токен Telegram-бота от [@BotFather](https://t.me/BotFather) | `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `POSTGRES_USER` | Имя пользователя PostgreSQL | `postgres` |
| `POSTGRES_PASSWORD` | Пароль от PostgreSQL | `my_secure_password` |
| `POSTGRES_DB` | Название базы данных | `bitrix_bot_db` |
| `POSTGRES_HOST` | Хост базы данных | `localhost` |
| `POSTGRES_PORT` | Порт PostgreSQL | `5432` |
| `YANDEX_OAUTH_TOKEN` | OAuth-токен Яндекс (для получения IAM) | `y0_AgAAAA...` |
| `YANDEX_IAM_TOKEN` | IAM-токен Яндекс Cloud (живёт 12 часов) | `t1.9euelZqZj5q...` |
| `YANDEX_FOLDER_ID` | ID каталога (folder) в Yandex Cloud | `b1gxxxxxxxxxxxxxxx` |
| `SELENIUM_HEADLESS` | Запускать браузер Chrome в фоновом режиме | `True` |

### Пример заполнения `.env`:

```env
# Telegram
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=MySecretPassword123
POSTGRES_DB=bitrix_bot_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Yandex Cloud
YANDEX_OAUTH_TOKEN=y0_AgAAAAA...
YANDEX_IAM_TOKEN=t1.9euelZqZj5qPk5iSkZqQj42MkZqN8_...
YANDEX_FOLDER_ID=b1g1234567890abcdef

# Selenium
SELENIUM_HEADLESS=True
```

## 📖 Использование

После запуска бота откройте Telegram и найдите своего бота по нику.

### Доступные команды:
- `/start` — приветствие и краткая инструкция

### Примеры запросов:
```
Как создать новый контакт в CRM?
Какие параметры нужны для метода crm.contact.add?
Как получить контакт по ID?
Покажи пример кода для создания контакта
```


## 📝 Обоснование выбора технологий

### Почему SQLAlchemy?
SQLAlchemy предоставляет мощный ORM-слой, который:
- Защищает от SQL-инъекций через параметризованные запросы
- Позволяет декларативно описывать модели через классы Python
- Обеспечивает переносимость между СУБД (SQLite для тестов → PostgreSQL для продакшена)
- Поддерживает связи между таблицами и отложенную загрузку

### Почему Selenium для парсинга?
Документация Bitrix24 использует динамическую подгрузку контента через JavaScript (SPA-элементы). Стандартная связка `requests` + `BeautifulSoup` не может получить полный текст таких страниц. Selenium гарантирует, что мы заберём весь отрендеренный DOM.

### Почему YandexGPT напрямую (без Assistants API)?
Прямой вызов YandexGPT через Foundation Models API даёт:
- Полный контроль над формированием контекста
- Хранение базы знаний в собственной PostgreSQL (независимость от вендора)
- Мгновенный SQL-поиск по документации вместо облачного RAG
- Использование той же модели YandexGPT 5

## 📄 Лицензия

Учебный проект. Создан в рамках практики по интеграции с Yandex Assistant.
