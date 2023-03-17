from flask_restful import Resource, marshal_with

from database.models import User, Trainer, Sport, SubUser, Subscription, Training
from serializers.crud import user_serializer, trainer_serializer, training_serializer, subscription_serializer, \
    sport_serializer, sub_user_serializer
from utils import create_blueprint_with_api, AdminResource

crud, api = create_blueprint_with_api("crud", "crud")


class UserCrud(AdminResource):
    def __init__(self):
        self.method_decorators.append(marshal_with(user_serializer))

    def get(self):
        return User.query.all()


class TrainerCrud(Resource):
    def __init__(self):
        self.method_decorators.append(marshal_with(trainer_serializer))

    def get(self):
        return Trainer.query.all()


class TrainingCrud(Resource):
    def __init__(self):
        self.method_decorators.append(marshal_with(training_serializer))

    @marshal_with(training_serializer)
    def get(self):
        return Training.query.all()


class SubscriptionCrud(Resource):
    def __init__(self):
        self.method_decorators.append(marshal_with(subscription_serializer))

    def get(self):
        return Subscription.query.all()


class SportCrud(Resource):
    def __init__(self):
        self.method_decorators.append(marshal_with(sport_serializer))

    def get(self):
        return Sport.query.all()


class SubscriptionUserCrud(Resource):
    def __init__(self):
        self.method_decorators.append(marshal_with(sub_user_serializer))

    def get(self):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import Session
        from flask import current_app

        engine = create_engine(current_app.config["SQLALCHEMY_DATABASE_URI"])
        with Session(engine) as session:
            return session.query(SubUser).all()


api.add_resource(UserCrud, '/users')
api.add_resource(TrainerCrud, '/trainers')
api.add_resource(TrainingCrud, '/trainings')
api.add_resource(SubscriptionCrud, '/subscriptions')
api.add_resource(SportCrud, '/sport')
api.add_resource(SubscriptionUserCrud, '/sub_user')
