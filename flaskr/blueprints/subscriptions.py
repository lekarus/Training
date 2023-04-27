from datetime import date

from database import db
from database.models import DailyTraining, PaymentStatus, Subscription, SubUser, Training, User
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import abort, Resource
from flask_restful_swagger import swagger
from flask_sqlalchemy.session import Session
from serializers.subscriptions import SubscriptionSchema, SubscriptionValidator, SubscriptionWithLinkSchema, \
    UserSubscribeValidator
import stripe
from utils import create_blueprint_with_api

subscriptions, api = create_blueprint_with_api("subscriptions", "subscriptions")


class SubscriptionsView(Resource):
    @staticmethod
    def _create_trainings(json: dict, daily_training, session):
        """create training instance"""
        trainings = [
            Training(
                daily_training_id=daily_training.id,
                description=training["description"],
                from_time=training["from_time"],
                to_time=training["to_time"],
            )
            for training in json
        ]
        session.bulk_save_objects(trainings)
        session.commit()

    def _create_daily_trainings(self, json, subscription, session):
        """create daily training instance"""
        for daily_training, counter in zip(json, range(len(json))):
            daily_training_instance = DailyTraining(
                subscription_id=subscription.id,
                description=daily_training["description"],
                rank=counter,
            )
            session.add(daily_training_instance)
            session.commit()
            self._create_trainings(daily_training["trainings"], daily_training_instance, session)

    def _create_subscription(self, json: dict, user: User, session) -> Subscription:
        """create subscription instance"""
        # create product on Stripe side
        product = stripe.Product.create(name=json["name"])
        cost_for_stripe = int(round(json["cost"], 2) * 100)
        price = stripe.Price.create(
            product=product["id"],
            unit_amount=cost_for_stripe,
            currency="uah",
            recurring={
                "interval": "day",
                "interval_count": json["period"],
            },
        )
        payment_link = stripe.PaymentLink.create(
            line_items=[
                {
                    "price": price["id"],
                    "quantity": 1,
                },
            ],
        )

        subscription = Subscription(
            trainer_id=user.trainer.id,
            name=json["name"],
            cost=json["cost"],
            period=json["period"],
            api_key=price["id"],
            link=payment_link["url"],
        )
        session.add(subscription)
        session.commit()
        self._create_daily_trainings(json["days"], subscription, session)
        return subscription

    def _validate(self, json) -> dict:
        """validation method"""
        errors = SubscriptionValidator().validate(json)
        if errors:
            return errors
        errors["days"] = dict()
        if len(json["days"]) != json["period"]:
            errors["days"]["err_message"] = "You must create days on each subscription day"

        for day, daily_counter in zip(json["days"], range(len(json["days"]))):  # enumeration of all days
            for training, counter in zip(day["trainings"], range(len(day["trainings"]))):
                # enumeration of all trainings in that day
                if training["from_time"] > training["to_time"]:
                    # check if the current workout starts after the end time
                    if not errors["days"].get(daily_counter):
                        errors["days"][daily_counter] = {"trainings": dict()}
                    # creating a skeleton for the dictionary so that there are no KeyErrors
                    errors["days"][daily_counter]["trainings"][counter] = "from_time must be after to_time"
        if not errors["days"]:
            errors = None
        return errors

    @swagger.operation(
        notes='Get all subscriptions',

        responseMessages=[
            {
                "code": 200,
                "message": "[List of subscriptions]",
            },
            {
                "code": 401,
                "message": "Missing Authorization Header",
            },
        ],
    )
    @jwt_required()
    def get(self):
        return SubscriptionSchema(many=True).dump(Subscription.query.all())

    @swagger.operation(
        notes='Create new subscription',
        parameters=[
            {
                "name": "name",
                "description": "subscription name",
                "required": True,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "body",
            }, {
                "name": "cost",
                "description": "subscription cost in UAH",
                "required": True,
                "allowMultiple": False,
                "dataType": float.__name__,
                "paramType": "body",
            }, {
                "name": "period",
                "description": "subscription duration",
                "required": True,
                "allowMultiple": False,
                "dataType": int.__name__,
                "paramType": "body",
            }, {
                "name": "days",
                "description": "a description of each day the subscription is valid",
                "required": True,
                "allowMultiple": True,
                "dataType": list.__name__,
                "paramType": "body",
            },
        ],
        responseMessages=[
            {
                "code": 201,
                "message": "[Subscription]",
            },
            {
                "code": 401,
                "message": "Missing Authorization Header",
            },
            {
                "code": 403,
                "message": "Access only for coaches",
            },
            {
                "code": 400,
                "message": "[Errors]",
            },
        ],
    )
    @jwt_required()
    def post(self):
        current_user = User.query.get(get_jwt_identity())
        if not current_user.is_trainer:
            abort(400, description="Access only for coaches")

        errors = self._validate(request.json)
        if errors:
            abort(400, **errors)
        with Session(db, expire_on_commit=False) as session:
            result = self._create_subscription(request.json, current_user, session)
            return SubscriptionSchema().dump(result)


class CheckActiveSubscriptions(Resource):
    """active subscriptions"""

    @swagger.operation(
        notes='Get your active subscriptions',
        responseMessages=[
            {
                "code": 200,
                "message": "[List of subscriptions]",
            },
            {
                "code": 401,
                "message": "Missing Authorization Header",
            },
        ],
    )
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


class CheckFutureSubscriptions(Resource):
    """future subscriptions"""

    @swagger.operation(
        notes='Get your future subscriptions',
        responseMessages=[
            {
                "code": 200,
                "message": "[List of subscriptions]",
            },
            {
                "code": 401,
                "message": "Missing Authorization Header",
            },
        ],
    )
    @jwt_required()
    def get(self):
        with Session(db) as session:
            sub_users = session.query(SubUser).filter(
                SubUser.c.user_id == get_jwt_identity(),
                SubUser.c.from_date > date.today(),
            ).all()
            subscriptions = session.query(Subscription).filter(
                Subscription.id.in_([sub.subscription_id for sub in sub_users]),
            ).all()
            return SubscriptionSchema(many=True).dump(subscriptions)


class SubscribeView(Resource):
    @swagger.operation(
        notes='Sign up for some subscription',
        parameters=[
            {
                "name": "from_date",
                "description": "your subscription start date",
                "required": True,
                "allowMultiple": False,
                "dataType": date.__name__,
                "paramType": "body",
            },
            {
                "name": "to_date",
                "description": "your subscription end date",
                "required": True,
                "allowMultiple": False,
                "dataType": date.__name__,
                "paramType": "body",
            },
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "[Subscription]",
            },
            {
                "code": 401,
                "message": "Missing Authorization Header",
            },
            {
                "code": 400,
                "message": "[Errors]",
            },
        ],
    )
    @jwt_required()
    def post(self, id):
        errors = UserSubscribeValidator().validate(request.json)
        if errors:
            return errors

        with Session(db) as session:
            insert_stmnt = SubUser.insert().values(
                user_id=get_jwt_identity(),
                subscription_id=id,
                from_date=request.json["from_date"],
                to_date=request.json["to_date"],
                payment_status=PaymentStatus.pending,
            )
            session.execute(insert_stmnt)
            session.commit()

        return SubscriptionWithLinkSchema().dump(Subscription.query.get(id))

    @swagger.operation(
        notes='Retrieve subscription',
        responseMessages=[
            {
                "code": 200,
                "message": "[Subscription]",
            },
            {
                "code": 401,
                "message": "Missing Authorization Header",
            },
        ],
    )
    @jwt_required()
    def get(self, id):
        sub = Subscription.query.get(id)
        return SubscriptionSchema().dump(sub)


api.add_resource(SubscriptionsView, '/')
api.add_resource(CheckActiveSubscriptions, '/active')
api.add_resource(CheckFutureSubscriptions, '/future')
api.add_resource(SubscribeView, '/subscribe/<int:id>')
