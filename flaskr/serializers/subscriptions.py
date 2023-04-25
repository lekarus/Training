from serializers import ma
from serializers.crud import TrainerSchema


class TrainingSchema(ma.Schema):
    class Meta:
        fields = ("id", "description", "from_time", "to_time")


class DailyTrainingSchema(ma.Schema):
    trainings = ma.Nested(TrainingSchema, many=True)

    class Meta:
        fields = ("id", "description", "rank", "trainings")


class SubscriptionSchema(ma.Schema):
    trainer = ma.Nested(TrainerSchema)
    days = ma.Nested(DailyTrainingSchema, many=True)

    class Meta:
        fields = ("id", "name", "cost", "period", "trainer", "days")


class TrainingValidator(ma.Schema):
    description = ma.String(required=True)
    from_time = ma.Time(required=True)
    to_time = ma.Time(required=True)


class DailyTrainingValidator(ma.Schema):
    description = ma.String(required=True)
    trainings = ma.Nested(TrainingValidator, required=True, many=True)


class SubscriptionValidator(ma.Schema):
    name = ma.String(required=True)
    cost = ma.Float(required=True)
    period = ma.Integer(required=True)
    days = ma.Nested(DailyTrainingValidator, required=True, many=True)
