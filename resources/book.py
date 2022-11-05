from models.book_model import BookModel

from flask_restful import Resource, reqparse


class Books(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="This field is required"
    )

    parser.add_argument(
        'book_cover',
        type=str,
        required=False,
    )

    parser.add_argument(
        'overview',
        type=str,
        required=True,
        help="This field is required"
    )

    parser.add_argument(
        'publication_date',
        type=str,
        required=True,
        help="This field is required"
    )

    parser.add_argument(
        'language',
        type=str,
        required=True,
        help="This field is required"
    )

    parser.add_argument(
        "b_id",
        type=int,
        required=False,
    )

    parser.add_argument(
        "a_id",
        type=int,
        required=True,
        help="Every book must have author id"
    )
    parser.add_argument(
        "g_id",
        type=int,
        required=True,
        help="Every book must have genre id"
    )

    @classmethod
    def post(cls):

        data = Books.parser.parse_args()

        book = BookModel.find_by_book_name(data['name'])

        if book:
            return {"Message": "A book with this name {} already exists.".format(data['name'])}, 400

        book = BookModel(data['name'], data['book_cover'], data['overview'], data['publication_date'], data['language'],
                         data["a_id"], data["g_id"])

        try:
            book.save_to_db()
        except:
            return {"Message": "An error occurred while inserting data"}, 500

        return book.json(), 201


class SearchByBookName(Resource):
    @classmethod
    def get(cls, name):
        book = BookModel.find_by_book_name(name)
        if book:
            return book.json()
        return {"Message": "Item Not found"}, 404


class BookList(Resource):
    @classmethod
    def get(cls):
        books = BookModel.query.all()
        return {"Books": [book.json() for book in books]}


class SearchByLang(Resource):
    @classmethod
    def get(cls, lang):
        books = BookModel.find_by_language(lang)

        if books:
            return {"Books": [book.json() for book in books]}
        return {"Message": "Item Not Found"}, 404


# class UpdateBookInfo(Resource):
#     def post(self):
#         data = Books.parser.parse_args()

#         book = BookModel.query.filter_by(b_id=data["b_id"]).update(
#            dict (b_name = data['name'] , 
#            book_cover = data['book_cover'], 
#            overview = data['overview'], 
#            publication_date = data['publication_date'], 
#            language = data['language'])
#         )
#         print('>>>>>>>>>>>>>>>>>')
#         print(book)
#         if book:
#             book.save_to_db()
#         return {"Message" : "Requested book-id doesn't exist."}, 404


class DeleteBook(Resource):
    @staticmethod
    def delete(b_id):
        book = BookModel.find_by_book_id(b_id)
        if book:
            book.delete_from_db()
        return {"Message": "Book remove successfully."}
