import sqlite3
from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help = 'this field cannot be left blank'
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help = 'this field cannot be left blank'
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        user = UserModel.find_by_username(data['username'])
        if user is not None:
            return {'message': 'User already exists'}, 400

        # user = UserModel(data['username'],data['password'])
        user = UserModel(**data) # here **data is same as above - it unpacks data... because we use a parser, we know that its gonna have sa username and password
        user.save_to_db()




        return {'message': 'User created successfully.'}, 201
