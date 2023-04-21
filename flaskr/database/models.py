import enum

from database import db
from sqlalchemy.dialects.postgresql import ENUM


class Roles(enum.Enum):
    admin = "admin"
    trainer = "trainer"
    student = "student"


class NotificationType(enum.Enum):
    to_all = "to_all"
    direct = "direct"
    subscription = "subscription"


SubUser = db.Table(
    'sub_user',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("subscription_id", db.Integer, db.ForeignKey("subscription.id")),
    db.Column('from_date', db.Date),
    db.Column('to_date', db.Date),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    role = db.Column(ENUM(Roles, name="role_enum"), nullable=False)

    subscriptions = db.relationship("Subscription", secondary=SubUser, backref="users", lazy='subquery')
    trainer = db.orm.relationship("Trainer", lazy='subquery', uselist=False)

    def __str__(self):
        return f"i am {self.first_name} {self.last_name}"

    def is_admin(self):
        return self.role == Roles.admin

    def is_trainer(self):
        return self.role == Roles.trainer


class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))


class Trainer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey("user.id"))
    sport_id = db.Column(db.ForeignKey("sport.id"))
    degree = db.Column(db.String(128))
    description = db.Column(db.String(128))

    sport = db.orm.relationship("Sport", backref="trainers", lazy='subquery')
    user = db.orm.relationship("User", lazy='subquery')


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trainer_id = db.Column(db.ForeignKey("trainer.id"))
    name = db.Column(db.String(128))
    cost = db.Column(db.Float(precision=2))
    period = db.Column(db.Integer)

    trainer = db.orm.relationship("Trainer", backref="subscriptions", lazy='subquery')


class DailyTraining(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subscription_id = db.Column(db.ForeignKey("subscription.id"))
    description = db.Column(db.String(128))
    rank = db.Column(db.Integer, autoincrement=True)

    subscription = db.orm.relationship("Subscription", backref="days", lazy='subquery')


class Training(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    daily_training_id = db.Column(db.ForeignKey("daily_training.id"))
    description = db.Column(db.String(128))
    from_time = db.Column(db.Time)
    to_time = db.Column(db.Time)

    daily_training = db.orm.relationship("DailyTraining", backref="trainings", lazy='subquery')


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_id = db.Column(db.ForeignKey("user.id"), nullable=True)
    to_id = db.Column(db.ForeignKey("user.id"))
    is_read = db.Column(db.Boolean)
    header = db.Column(db.String(64))
    body = db.Column(db.Text)
    send_at = db.Column(db.DateTime)
