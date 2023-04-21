from auth.auth import admin_required
from database.models import Roles, Sport, Subscription, SubUser, Trainer, Training, User
from flask_restful import reqparse, Resource
from serializers import crud_schemas
from serializers import serializer_decorator
from utils import AdminResource, create_blueprint_with_api, CRUDResource, CRUDRetrieveResource, mail_checker
from werkzeug.http import http_date
from werkzeug.security import generate_password_hash


crud, api = create_blueprint_with_api("crud", "crud")


class UserCrud(AdminResource, CRUDResource):
    method_decorators = [admin_required(), serializer_decorator(crud_schemas.users_schema)]

    def __init__(self):
        self.table = User

        super().__init__()

    def load_parser(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=mail_checker, location='json', required=True)
        self.reqparse.add_argument('password', type=str, location='json', required=True)
        self.reqparse.add_argument('first_name', type=str, location='json', required=True)
        self.reqparse.add_argument('last_name', type=str, location='json', required=True)
        self.reqparse.add_argument('role', type=Roles, choices=list(Roles), location='json', required=True)
        self.reqparse.add_argument('password', type=str, location='json', required=True)
        self.args = self.reqparse.parse_args()
        self.args["password"] = generate_password_hash(self.args["password"])


class UserRetrieveCrud(AdminResource, CRUDRetrieveResource):
    method_decorators = [admin_required(), serializer_decorator(crud_schemas.user_schema)]

    def __init__(self):
        self.table = User

        super().__init__()

    def load_parser(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=mail_checker, location='json', required=True)
        self.reqparse.add_argument('password', type=str, location='json', required=True)
        self.reqparse.add_argument('first_name', type=str, location='json', required=True)
        self.reqparse.add_argument('last_name', type=str, location='json', required=True)
        self.reqparse.add_argument('role', type=Roles, choices=list(Roles), location='json', required=True)
        self.reqparse.add_argument('password', type=str, location='json', required=True)
        self.args = self.reqparse.parse_args()
        self.args["password"] = generate_password_hash(self.args["password"])


class TrainerCrud(AdminResource, CRUDResource):
    method_decorators = [admin_required(), serializer_decorator(crud_schemas.trainers_schema)]

    def __init__(self):
        self.table = Trainer

        super().__init__()

    def load_parser(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_id', type=int, location='json', required=True)
        self.reqparse.add_argument('sport_id', type=int, location='json', required=True)
        self.reqparse.add_argument('degree', type=str, location='json', required=True)
        self.reqparse.add_argument('description', type=str, location='json', required=True)
        self.args = self.reqparse.parse_args()


class TrainerCrudRetrieve(AdminResource, CRUDRetrieveResource):
    method_decorators = [admin_required(), serializer_decorator(crud_schemas.trainer_schema)]

    def __init__(self):
        self.table = Trainer

        super().__init__()

    def load_parser(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_id', type=int, location='json', required=True)
        self.reqparse.add_argument('sport_id', type=int, location='json', required=True)
        self.reqparse.add_argument('degree', type=str, location='json', required=True)
        self.reqparse.add_argument('description', type=str, location='json', required=True)
        self.args = self.reqparse.parse_args()


class TrainingCrud(AdminResource, CRUDResource):
    method_decorators = [admin_required(), serializer_decorator(crud_schemas.trainings_schema)]

    def __init__(self):
        self.table = Training

        super().__init__()

    def load_parser(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('trainer_id', type=int, location='json', required=True)
        self.reqparse.add_argument('description', type=str, location='json', required=True)
        self.args = self.reqparse.parse_args()


class TrainingCrudRetrieve(AdminResource, CRUDRetrieveResource):
    method_decorators = [admin_required(), serializer_decorator(crud_schemas.training_schema)]

    def __init__(self):
        self.table = Training

        super().__init__()

    def load_parser(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('trainer_id', type=int, location='json', required=True)
        self.reqparse.add_argument('description', type=str, location='json', required=True)
        self.args = self.reqparse.parse_args()


class SubscriptionCrud(AdminResource, CRUDResource):
    method_decorators = [admin_required(), serializer_decorator(crud_schemas.subscriptions_schema)]

    def __init__(self):
        self.table = Subscription

        super().__init__()

    def load_parser(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('trainer_id', type=int, location='json', required=True)
        self.reqparse.add_argument('name', type=str, location='json', required=True)
        self.reqparse.add_argument('cost', type=float, location='json', required=True)
        self.reqparse.add_argument('period', type=int, location='json', required=True)
        self.args = self.reqparse.parse_args()


class SubscriptionCrudRetrieve(AdminResource, CRUDRetrieveResource):
    method_decorators = [admin_required(), serializer_decorator(crud_schemas.subscription_schema)]

    def __init__(self):
        self.table = Subscription

        super().__init__()

    def load_parser(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('trainer_id', type=int, location='json', required=True)
        self.reqparse.add_argument('name', type=str, location='json', required=True)
        self.reqparse.add_argument('cost', type=float, location='json', required=True)
        self.reqparse.add_argument('period', type=int, location='json', required=True)
        self.args = self.reqparse.parse_args()


class SportCrud(AdminResource, CRUDResource):
    method_decorators = [admin_required(), serializer_decorator(crud_schemas.sports_schema)]

    def __init__(self):
        self.table = Sport

        super().__init__()

    def load_parser(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json', required=True)
        self.args = self.reqparse.parse_args()


class SportCrudRetrieve(AdminResource, CRUDRetrieveResource):
    method_decorators = [admin_required(), serializer_decorator(crud_schemas.sport_schema)]

    def __init__(self):
        self.table = Sport

        super().__init__()

    def load_parser(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json', required=True)
        self.args = self.reqparse.parse_args()


class SubscriptionUserCrud(AdminResource, CRUDResource):
    method_decorators = [admin_required(), serializer_decorator(crud_schemas.sub_users_schema)]

    def __init__(self):
        self.table = SubUser

        super().__init__()

    def load_parser(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_id', type=int, location='json', required=True)
        self.reqparse.add_argument('subscription_id', type=int, location='json', required=True)
        self.reqparse.add_argument('from_date', type=http_date, location='json', required=True)
        self.reqparse.add_argument('to_date', type=http_date, location='json', required=True)
        self.args = self.reqparse.parse_args()


class SubscriptionUserCrudRetrieve(AdminResource, CRUDRetrieveResource):
    method_decorators = [admin_required(), serializer_decorator(crud_schemas.sub_user_schema)]

    def __init__(self):
        self.table = SubUser

        super().__init__()

    def load_parser(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_id', type=int, location='json', required=True)
        self.reqparse.add_argument('subscription_id', type=int, location='json', required=True)
        self.reqparse.add_argument('from_date', type=http_date, location='json', required=True)
        self.reqparse.add_argument('to_date', type=http_date, location='json', required=True)
        self.args = self.reqparse.parse_args()


class TestResource(Resource):
    def get(self):
        return "200"


api.add_resource(UserCrud, '/users')
api.add_resource(UserRetrieveCrud, '/users/<int:instance_id>')

api.add_resource(TrainerCrud, '/trainers')
api.add_resource(TrainerCrudRetrieve, '/trainers/<int:instance_id>')

api.add_resource(TrainingCrud, '/trainings')
api.add_resource(TrainingCrudRetrieve, '/trainings/<int:instance_id>')

api.add_resource(SubscriptionCrud, '/subscriptions')
api.add_resource(SubscriptionCrudRetrieve, '/subscriptions/<int:instance_id>')

api.add_resource(SportCrud, '/sports')
api.add_resource(SportCrudRetrieve, '/sports/<int:instance_id>')

api.add_resource(SubscriptionUserCrud, '/sub_users')
api.add_resource(SubscriptionUserCrudRetrieve, '/sub_users/<int:instance_id>')

api.add_resource(TestResource, '/test')
