from flask_jwt_extended import create_access_token, create_refresh_token
from flask import jsonify
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash

from database.models import User
from utils import create_blueprint_with_api

auth, api = create_blueprint_with_api("auth", url_prefix="auth")


class Login(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, location='json', required=True)
        self.reqparse.add_argument('password', type=str, location='json', required=True)
        super(Resource, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        user = User.query.filter_by(email=args["email"]).first()
        if not user or not check_password_hash(user.password, args["password"]):
            return {"msg": "Bad username or password"}, 401

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify(access_token=access_token, refresh_token=refresh_token)


api.add_resource(Login, "/login")
