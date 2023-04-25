from database.models import Subscription, User
from marshmallow import fields
from serializers import ma


class UserSchema(ma.Schema):
    role = fields.Method("get_role")

    def get_role(self, value):
        return value.role.value

    class Meta:
        fields = ("id", "first_name", "last_name", "email", "role")


class SportSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")


class TrainerSchema(ma.Schema):
    user = ma.Nested(UserSchema)
    sport = ma.Nested(SportSchema)

    class Meta:
        fields = ("id", "user", "sport", "degree", "description")


class TrainingSchema(ma.Schema):

    class Meta:
        fields = ("id", "daily_training_id", "description", "from_time", "to_time")


class SubscriptionSchema(ma.Schema):
    trainer = ma.Nested(TrainerSchema)

    class Meta:
        fields = ("id", "trainer", "name", "cost", "period")


class SubscriptionUserSchema(ma.Schema):
    user = fields.Method("get_user")
    subscription = fields.Method("get_subscription")

    def get_user(self, obj):
        return UserSchema().dump(User.query.filter_by(id=obj.user_id).first())

    def get_subscription(self, obj):
        return SubscriptionSchema().dump(Subscription.query.filter_by(id=obj.subscription_id).first())

    class Meta:
        fields = ("id", "user", "subscription", "from_date", "to_date")
