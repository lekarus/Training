from flask_restful import fields, marshal_with

from database.models import Subscription, User


class Date(fields.Raw):
    def format(self, value):
        return value.strftime('%Y-%m-%d')


user_serializer = {
    "id": fields.Integer,
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String
}


class NestedUser(fields.Raw):
    @marshal_with(user_serializer)
    def format(self, value):
        return User.query.filter_by(id=value).all()


trainer_serializer = {
    "id": fields.Integer,
    "user": fields.Nested(user_serializer),
    "sport": fields.String(attribute="sport.sport"),
    "degree": fields.String,
    "description": fields.String
}

training_serializer = {
    "id": fields.Integer,
    "trainer": fields.Nested(trainer_serializer),
    "description": fields.String
}

subscription_serializer = {
    "id": fields.Integer,
    "trainer": fields.Nested(trainer_serializer),
    "sub_name": fields.String,
    "cost": fields.Float,
    "period": fields.Integer
}


class NestedSubscription(fields.Raw):
    @marshal_with(subscription_serializer)
    def format(self, value):
        return Subscription.query.filter_by(id=value).all()


sport_serializer = {
    "id": fields.Integer,
    "sport": fields.String
}

sub_user_serializer = {
    "id": fields.Integer,
    "user_id": NestedUser,
    "subscription_id": NestedSubscription,
    "from_date": Date,
    "to_date": Date
}
