from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource, reqparse

from models.user_model import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field can't be empty."
    )

    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field can't be empty"
    )

    parser.add_argument(
        'role',
        type=int,
        required=True,
        help="This field can't be empty."
    )

    @classmethod
    def post(cls):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"Message": "A username with this name is already exist."}, 400

        user = UserModel(data["username"], data["password"], data["role"])
        user.save_to_db()

        return {"Message": "User created successfully."}, 201


class UserList(Resource):
    @classmethod
    def get(cls):
        users = UserModel.query.all()
        return {"users": [user.json() for user in users]}


class User(Resource):

    @classmethod
    def get(cls, uid):
        user = UserModel.find_by_user_id(uid)
        if not user:
            return {"Message": "User not Found!"}, 404
        return user.json()

    @classmethod
    def delete(cls, uid):
        user = UserModel.find_by_user_id(uid)
        if not user:
            return {"Message": "User not Found!"}, 404

        user.delete_from_db()
        return {"Message": "User deleted successfully"}, 200


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field can't be empty."
    )

    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field can't be empty"
    )

    @classmethod
    def post(cls):
        data = UserLogin.parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user and user.password == data['password']:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {
                       "access_token": access_token,
                       "refresh_token": refresh_token
                   }, 200

        return {"Message": "Invalid User Credentials"}, 401
