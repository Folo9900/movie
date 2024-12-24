# Movie Finder

Веб-сервис для подбора фильмов на вечер с интеграцией Telegram бота.

## Особенности

- Бесконечная лента фильмов с постерами и описаниями
- Фильтрация по году, жанру и стране
- Рейтинги с IMDb и Кинопоиска
- Кнопка "Мне повезёт" для случайного выбора фильма
- Интеграция с Telegram ботом

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/movie-finder.git
cd movie-finder
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл .env на основе .env.example и заполните необходимые переменные окружения:
```
TELEGRAM_TOKEN=your_telegram_bot_token
APP_URL=your_app_url
TMDB_API_KEY=your_tmdb_api_key
```

4. Импортируйте фильмы:
```bash
python import_movies.py
```

5. Запустите приложение:
```bash
python app.py
```

## Развертывание

Приложение готово к развертыванию на Render.com. Подробные инструкции в документации.

## Технологии

- Flask
- SQLAlchemy
- TMDB API
- python-telegram-bot
- Bootstrap 5

## Лицензия

MIT
