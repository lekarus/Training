from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    password = db.Column(db.String(128))
    subscriptions = db.orm.relationship("Subscription", secondary="SubUser", back_populates="users")


class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sport = db.Column(db.String(128))


class Trainer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey("user.id"))
    sport_id = db.Column(db.ForeignKey("sport.id"))

    sport = db.orm.relationship("Sport", back_populates="trainers")
    user = db.orm.relationship("User")


class Training(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trainer_id = db.Column(db.ForeignKey("trainer.id"))
    description = db.Column(db.String(128))

    trainer = db.orm.relationship("Trainer", back_populates="workouts")


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trainer_id = db.Column(db.ForeignKey("trainer.id"))
    sub_name = db.Column(db.String(128))
    cost = db.Column(db.Float(precision=2))
    period = db.Column(db.Integer)

    trainer = db.orm.relationship("Trainer", back_populates="subscriptions")


class SubUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.ForeignKey("user.id")),
    subscription = db.Column(db.ForeignKey("subscription.id")),
    from_date = db.Column(db.Date())
    to_date = db.Column(db.Date())

