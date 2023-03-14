from flask_restful import fields


user_serializer = {
    "id": fields.Integer,
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String
}


trainer_serializer = {
    "user": fields.Nested(user_serializer),
    "sport": fields.String(attribute="sport.sport"),
    "degree": fields.String,
    "description": fields.String
}


training_serializer = {
    "trainer": fields.Nested(trainer_serializer),
    "description": fields.String
}


subscription_serializer = {
    "trainer": fields.Nested(trainer_serializer),
    "abon_name": fields.String,
    "value": fields.Float,
    "period": fields.Integer
}
