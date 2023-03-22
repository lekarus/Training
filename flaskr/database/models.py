import enum

from sqlalchemy.dialects.postgresql import ENUM

from database import db


class Roles(enum.Enum):
    admin = "admin"
    trainer = "trainer"
    student = "student"


SubUser = db.Table(
    'sub_user',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("subscription_id", db.Integer, db.ForeignKey("subscription.id")),
    db.Column('from_date', db.Date),
    db.Column('to_date', db.Date)
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    role = db.Column(ENUM(Roles, name="role_enum"), nullable=False, )

    subscriptions = db.orm.relationship("Subscription", secondary=SubUser, backref="users", lazy='subquery')

    def __str__(self):
        return f"i am {self.first_name} {self.last_name}"

    def is_admin(self):
        return self.role == Roles.admin


class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sport = db.Column(db.String(128))


class Trainer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey("user.id"))
    sport_id = db.Column(db.ForeignKey("sport.id"))
    degree = db.Column(db.String(128))
    description = db.Column(db.String(128))

    sport = db.orm.relationship("Sport", backref="trainers", lazy='subquery')
    user = db.orm.relationship("User", lazy='subquery')


class Training(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trainer_id = db.Column(db.ForeignKey("trainer.id"))
    description = db.Column(db.String(128))

    trainer = db.orm.relationship("Trainer", backref="workouts", lazy='subquery')


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trainer_id = db.Column(db.ForeignKey("trainer.id"))
    sub_name = db.Column(db.String(128))
    cost = db.Column(db.Float(precision=2))
    period = db.Column(db.Integer)

    trainer = db.orm.relationship("Trainer", backref="subscriptions", lazy='subquery')
