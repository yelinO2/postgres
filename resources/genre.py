from models.genre_model import GenreModel

from flask_restful import Resource, reqparse


class Genre(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help='This field cannot be empty.'
    )

    @classmethod
    def post(cls):

        data = Genre.parser.parse_args()
        author = GenreModel.find_by_genre_name(data['name'])

        if author:
            return {"Message": "{} already exists.".format(data['name'])}, 400

        author = GenreModel(data['name'])
        try:
            author.save_to_db()
        except:
            {"Message": "Error occurs."}, 404

        return author.json(), 201


class GenreList(Resource):
    @classmethod
    def get(cls):
        genre = GenreModel.query.all()
        return {"Genre List": [g.json() for g in genre]}


class SearchGenre(Resource):
    @classmethod
    def get(cls, genre):
        genre = GenreModel.find_by_genre_name(genre)
        if genre:
            return genre.json()
        return {"Message": "Genre Not Found"}, 404
