from database.models import User
from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import reqparse, Resource
from flask_restful_swagger import swagger
from utils import create_blueprint_with_api
from werkzeug.security import check_password_hash

auth, api = create_blueprint_with_api("auth", url_prefix="auth")


class Login(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, location='json', required=True)
        self.reqparse.add_argument('password', type=str, location='json', required=True)
        super(Resource, self).__init__()

    @swagger.operation(
        notes='Login',
        parameters=[
            {
                "name": "username",
                "description": "username",
                "required": True,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "body",
            },
            {
                "name": "password",
                "description": "password",
                "required": True,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "body",
            },
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "[access_token], [refresh_token]",
            },
            {
                "code": 401,
                "message": "Bad username or password",
            },
        ],
    )
    def post(self):
        args = self.reqparse.parse_args()
        user = User.query.filter_by(email=args["email"]).first()
        if not user or not check_password_hash(user.password, args["password"]):
            return {"msg": "Bad username or password"}, 401

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify(access_token=access_token, refresh_token=refresh_token)


api.add_resource(Login, "/login")
