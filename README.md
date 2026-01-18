# Film Search Application

Приложение для поиска и фильтрации фильмов с аналитикой поисковых запросов.

## Стек технологий

- **Backend**: FastAPI + Uvicorn
- **Database**: MySQL (основная БД), MongoDB (аналитика запросов)
- **Frontend**: Jinja2 templates + Bootstrap CSS
- **Python**: 3.8+

## Требования

- Python 3.8+
- MySQL 5.7+
- MongoDB 4.0+

## Установка и настройка

### 1. Клонируйте репозиторий и установите зависимости

```bash
pip install -r requirements.txt
```

### 2. Настройте переменные окружения

Скопируйте файл `.env.example` в `.env` и заполните реальные значения:

```bash
cp .env.example .env
```

Отредактируйте `.env` с ваши учетными данными:

```env
MYSQL_HOST=ваш_хост
MYSQL_USER=ваше_имя
MYSQL_PASSWORD=ваш_пароль
MYSQL_DB=имя_базы
MONGODB_URL_EDIT=mongodb://хост:порт
```

### 3. Запустите сервер

**Для разработки:**
```bash
python main.py
```

**Для продакшина (через Gunicorn):**
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

Приложение будет доступно по адресу: `http://localhost:8000`

## Функциональность

### Основные страницы

- **/** - Главная страница с каталогом фильмов и жанрами
- **/genre/{name}** - Фильмы выбранного жанра с фильтрацией по годам
- **/analytics** - Статистика популярных и недавних поисков
- **/analytics/data** - API для получения данных аналитики (JSON)

### Поиск и фильтрация

- **Поиск по названию** - `/search_title` (POST)
- **Фильтр по жанру и годам** - `/search_filter` (POST)

### Пагинация

Все результаты пагинированы (10 элементов на странице).

## Исправления и оптимизации (v2.0)

✅ **Критические исправления:**
- Исправлена опечатка в `search_by_title()` (`get_db_conneсt` → `get_db_connet`)
- Исправлена синтаксическая ошибка в `new_films()`

✅ **Безопасность:**
- Добавлена валидация input'ов (номера страниц, годы)
- Экранирование одинарных кавычек в SQL запросах
- Ограничение длины строк поиска (100 символов)
- Ограничение лимита аналитики (максимум 100 запросов)

✅ **Оптимизация кода:**
- Удалены дублирования SQL запросов через функцию `_get_films_base_query()`
- Добавлена обработка ошибок во всех эндпоинтах
- Добавлено логирование для отладки

✅ **Пагинация:**
- Исправлена пагинация для сохранения параметров фильтра при переходе между страницами
- Улучшены шаблоны для предотвращения перехода на несуществующие страницы

✅ **Production-ready:**
- Добавлена система логирования
- Обработка исключений на всех уровнях
- CORS настройка (в продакшине замените на конкретные домены)
- Документированы конфиги для разных окружений

## Структура проекта

```
.
├── main.py                 # Основное приложение FastAPI
├── requirements.txt        # Зависимости Python
├── .env.example           # Шаблон переменных окружения
├── README.md              # Этот файл
├── databases/
│   ├── db_mysql.py        # Функции для работы с MySQL
│   └── db_mongo.py        # Функции для работы с MongoDB
├── templates/             # HTML шаблоны Jinja2
│   ├── base.html
│   ├── index.html
│   ├── results.html
│   ├── analytics.html
│   └── recent.html
└── static/                # Статические файлы
    ├── style.css
    ├── bootstrap.min.css
    └── images/
```

## Развертывание на продакшине

### Рекомендуемая конфигурация для Ubuntu/CentOS:

1. **Используйте Gunicorn + Nginx в reverse proxy**
2. **Настройте systemd сервис:**

```ini
[Unit]
Description=Film Search API
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/app
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind unix:/tmp/app.sock \
    main:app

[Install]
WantedBy=multi-user.target
```

3. **Конфиг Nginx:**

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://unix:/tmp/app.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Решение проблем

### MongoDB не подключается
- Проверьте, что MongoDB запущена: `mongod --version`
- Проверьте строку подключения в `.env`

### MySQL ошибка подключения
- Убедитесь, что MySQL запущена: `mysql --version`
- Проверьте учетные данные в `.env`

### Поиск не работает
- В `db_mysql.py` исправлена опечатка `get_db_conneсt()` → `get_db_connet()`
- Перезагрузите сервер

## Лицензия

MIT

## Автор

Sergii Lanovenkyi (@ichprojekt)
