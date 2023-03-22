from serializers.crud import UserSchema, TrainerSchema, TrainingSchema, SubscriptionSchema, SportSchema, \
    SubscriptionUserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)

trainer_schema = TrainerSchema()
trainers_schema = TrainerSchema(many=True)

training_schema = TrainingSchema()
trainings_schema = TrainingSchema(many=True)

subscription_schema = SubscriptionSchema()
subscriptions_schema = SubscriptionSchema(many=True)

sport_schema = SportSchema()
sports_schema = SportSchema(many=True)

sub_user_schema = SubscriptionUserSchema()
sub_users_schema = SubscriptionUserSchema(many=True)
