from flask import Blueprint
from flask_restful import Api, Resource

from auth.auth import admin_required


def create_blueprint_with_api(print_name, url_prefix=None):
    blueprint = Blueprint(print_name, __name__, url_prefix="/" + url_prefix)
    api = Api(blueprint)
    return blueprint, api


class AdminResource(Resource):
    method_decorators = [admin_required()]
