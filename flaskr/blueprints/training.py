from datetime import date

from database import db
from database.models import Subscription, SubUser
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask_sqlalchemy.session import Session
from serializers.crud import SubscriptionSchema
from utils import create_blueprint_with_api


training, api = create_blueprint_with_api("training")


class CheckActiveSubscriptions(Resource):
    @jwt_required()
    def get(self):
        with Session(db) as session:
            sub_users = session.query(SubUser).filter(
                SubUser.c.user_id == get_jwt_identity(),
                SubUser.c.from_date < date.today(),
                SubUser.c.to_date > date.today(),
            ).all()
            subscriptions = session.query(Subscription).filter(
                Subscription.id.in_([sub.subscription_id for sub in sub_users]),
            ).all()
        return SubscriptionSchema(many=True).dump(subscriptions)


api.add_resource(CheckActiveSubscriptions, '/active_subscriptions')
