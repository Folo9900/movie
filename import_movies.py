from tmdbv3api import TMDb, Movie
from app import app, db, Movie as MovieModel
import os
from dotenv import load_dotenv

load_dotenv()

def import_movies():
    # Инициализация TMDB
    tmdb = TMDb()
    tmdb.api_key = os.getenv('TMDB_API_KEY')
    tmdb.language = 'ru'  # Русский язык для описаний
    
    movie = Movie()
    
    # Получаем популярные фильмы
    popular_movies = movie.popular()
    
    with app.app_context():
        for tmdb_movie in popular_movies:
            # Получаем детальную информацию о фильме
            details = movie.details(tmdb_movie.id)
            
            # Получаем рейтинги
            imdb_rating = details.vote_average
            # Для примера используем тот же рейтинг для Кинопоиска
            kinopoisk_rating = imdb_rating
            
            # Создаем запись в базе данных
            movie_entry = MovieModel(
                title=details.title,
                description=details.overview,
                year=int(details.release_date[:4]) if details.release_date else None,
                genre=', '.join([genre['name'] for genre in details.genres]),
                country=details.production_countries[0]['name'] if details.production_countries else 'Неизвестно',
                poster_url=f"https://image.tmdb.org/t/p/w500{details.poster_path}" if details.poster_path else None,
                imdb_rating=imdb_rating,
                kinopoisk_rating=kinopoisk_rating
            )
            
            # Проверяем, нет ли уже такого фильма
            existing_movie = MovieModel.query.filter_by(title=movie_entry.title).first()
            if not existing_movie:
                db.session.add(movie_entry)
        
        db.session.commit()
        print("Импорт фильмов завершен!")

if __name__ == '__main__':
    import_movies()
