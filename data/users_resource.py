from flask_restful import Resource
from data import db_session
from data.user import User
from flask import abort, jsonify
from data.user_pase import parser
from werkzeug.security import generate_password_hash


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found.")
    return session


class UsersResource(Resource):
    def get(self, user_id):
        session = abort_if_user_not_found(user_id)
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('nickname', 'age', 'position', 'address', 'email', 'password'))})

    def delete(self, user_id):
        session = abort_if_user_not_found(user_id)
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        return jsonify({'out': 'Нет функции put'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict() for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User()
        user.nickname = args['nickname']
        user.set_password(args['password'])
        user.age = args['age']
        user.position = args['position']
        user.address = args['address']
        user.email = args['email']
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})