from flask import request, jsonify
from flask_restx import Resource, Namespace, fields

from app.container import movies_service
from app.dao.schema.movie import MovieSchema

movie_ns = Namespace('movies')  # создаем namespace фильмов

movie_schema = MovieSchema()  # схема для сериализации одного фильма в словарь
movies_schema = MovieSchema(many=True)  # схема для сериализации нескольких фильмов в список словарей


# movie_model = movie_ns.model('Movies',
#                              {
#                                  'title': fields.String(required=True),
#                                  'description': fields.String(required=True),
#                                  'trailer': fields.String(required=True),
#                                  'year': fields.Integer(required=True),
#                                  'rating': fields.Float(required=True),
#                                  'genre_id': fields.Integer(required=True),
#                                  'director_id': fields.Integer(required=True)
#                              })


@movie_ns.route('/')
class MoviesView(Resource):
    """
    CBV фильмов
    GET - получение данных всех фильмов,
    фильмов по жанрам, режиссерам или году выпуска
    POST - добавление данных нового фильма
    """

    # создаем документацию и параметры для GET
    @movie_ns.doc(
        description='Оставьте поля пустыми для вывода всех данных\n'
                    'при заполнения id режиссера выведутся данные фильмов по id режиссера\n'
                    'при заполнения id жанра выведутся данные фильмов по id жанра\n'
                    'при заполнения года выпуска выведутся данные фильмов по году выпуска\n',
        params={
            'director_id': 'id режиссера',
            'genre_id': 'id жанра',
            'year': 'год выпуска'
        }
    )
    def get(self):

        director_id = request.args.get('director_id', type=int)  # получаем id режиссера
        genre_id = request.args.get('genre_id', type=int)  # получаем id жанра
        year = request.args.get('year', type=int)  # получаем год выпуска

        # поиск по id режиссера
        if director_id:
            movies = movies_service.get_by_directors(director_id)

        # поиск по id жанра
        elif genre_id:
            movies = movies_service.get_by_genres(genre_id)

        # поиск по году выпуска
        elif year:
            movies = movies_service.get_by_years(year)

        # вывод всех фильмов
        else:
            movies = movies_service.get_all()
        if not movies:
            return "NotFound", 404
        return movies_schema.dump(movies), 200

    # @movie_ns.doc(description="Заполните данные нового фильма в json формате", body=movie_model)
    def post(self):

        new_movie_json = request.json
        try:
            new_movie = movies_service.create(new_movie_json)
        except TypeError as e:
            return str(e), 400
        response = jsonify(movie_schema.dump(new_movie))
        response.status_code = 201
        response.headers['location'] = new_movie.id  # добавляем location в заголовок
        return response


@movie_ns.route('/<int:movie_id>/')
class MovieView(Resource):
    """
    CBV фильма
    GET - получение данных фильма по id
    PUT - обновление данных фильма по id
    PATCH - частичное обновление данных по id
    DELETE - удаление фильма по id
    каждый метод в случае ошибки выдаст ошибку 404
    """

    def get(self, movie_id):
        movie = movies_service.get_one(movie_id)
        return movie_schema.dump(movie), 200

    def put(self, movie_id):
        update_json = request.json

        try:
            movies_service.check_is_dict(update_json)
            if not update_json.get('id'):
                update_json['id'] = movie_id
            movie = movies_service.update(movie_id, update_json)
        except TypeError as e:
            return str(e), 400

        return movie_schema.dump(movie), 201

    def patch(self, movie_id):
        update_json = request.json

        try:
            movies_service.check_is_dict(update_json)
            if not update_json.get('id'):
                update_json['id'] = movie_id
            movie = movies_service.update_partial(movie_id, update_json)
        except TypeError as e:
            return str(e), 400

        return movie_schema.dump(movie), 201

    def delete(self, movie_id):
        movies_service.delete(movie_id)
        return '', 204
