from models.author_model import AuthorModel

from flask_restful import Resource, reqparse


class Authors(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help='This field cannot be empty.'
    )

    @staticmethod
    def post():

        data = Authors.parser.parse_args()
        author = AuthorModel.find_by_author_name(data['name'])

        if author:
            return {"Message": "{} already exists.".format(data['name'])}, 400

        author = AuthorModel(data['name'])
        try:
            author.save_to_db()
        except:
            {"Message": "Error occurs."}, 404

        return author.json(), 201


class AuthorList(Resource):
    @staticmethod
    def get():
        authors = AuthorModel.query.all()
        return {"Author": [author.json() for author in authors]}


class SearchAuthor(Resource):
    @staticmethod
    def get(author):
        author = AuthorModel.find_by_author_name(author)
        if author:
            return author.json()
        return {"Message": "Author Not found"}, 404
