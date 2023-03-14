from flask import Blueprint
from flask_restful import Api, Resource, marshal_with

from database.models import User, Trainer
from serializers.crud import user_serializer, trainer_serializer, training_serializer, subscription_serializer

crud = Blueprint('crud', __name__, template_folder='templates', url_prefix="/crud")
api = Api(crud)


class UserCrud(Resource):
    @marshal_with(user_serializer)
    def get(self):
        return User.query.all()


class TrainerCrud(Resource):
    @marshal_with(trainer_serializer)
    def get(self):
        return Trainer.query.all()


class TrainingCrud(Resource):
    @marshal_with(training_serializer)
    def get(self):
        return User.query.all()


class SubscriptionCrud(Resource):
    @marshal_with(subscription_serializer)
    def get(self):
        return User.query.all()


api.add_resource(UserCrud, '/users')
api.add_resource(TrainerCrud, '/trainers')
api.add_resource(TrainingCrud, '/trainings')
api.add_resource(SubscriptionCrud, '/subscriptions')
