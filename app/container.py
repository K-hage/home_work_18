from app.dao.directors import DirectorsDAO
from app.dao.genres import GenresDAO
from app.dao.movies import MoviesDAO
from app.service.directors import DirectorsService
from app.service.genres import GenresService
from app.service.movies import MoviesService
from app.setup_db import db

movies_dao = MoviesDAO(db.session)  # создаем экземпляр DAO фильмов
movies_service = MoviesService(movies_dao)  # создаем экземпляр сервиса фильмов

genres_dao = GenresDAO(db.session)  # создаем экземпляр DAO жанров
genres_service = GenresService(genres_dao)  # создаем экземпляр сервиса жанров

directors_dao = DirectorsDAO(db.session)  # создаем экземпляр DAO режиссеров
directors_service = DirectorsService(directors_dao)  # создаем экземпляр сервиса режиссеров
