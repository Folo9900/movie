from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import random
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer)
    genre = db.Column(db.String(100))
    country = db.Column(db.String(100))
    poster_url = db.Column(db.String(500))
    imdb_rating = db.Column(db.Float)
    kinopoisk_rating = db.Column(db.Float)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/movies')
def get_movies():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    query = Movie.query
    
    # Применяем фильтры
    genre = request.args.get('genre')
    year = request.args.get('year')
    country = request.args.get('country')
    
    if genre:
        query = query.filter(Movie.genre.contains(genre))
    if year:
        query = query.filter(Movie.year == year)
    if country:
        query = query.filter(Movie.country == country)
        
    movies = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'movies': [{
            'id': movie.id,
            'title': movie.title,
            'description': movie.description,
            'poster_url': movie.poster_url,
            'imdb_rating': movie.imdb_rating,
            'kinopoisk_rating': movie.kinopoisk_rating,
            'year': movie.year,
            'genre': movie.genre,
            'country': movie.country
        } for movie in movies.items],
        'has_next': movies.has_next
    })

@app.route('/api/random')
def get_random_movie():
    movie = Movie.query.filter(
        Movie.imdb_rating >= 5
    ).order_by(db.func.random()).first()
    
    return jsonify({
        'id': movie.id,
        'title': movie.title,
        'description': movie.description,
        'poster_url': movie.poster_url,
        'imdb_rating': movie.imdb_rating,
        'kinopoisk_rating': movie.kinopoisk_rating,
        'year': movie.year,
        'genre': movie.genre,
        'country': movie.country
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
