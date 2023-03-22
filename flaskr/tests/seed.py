from database import db
from database.models import Sport, Subscription, Trainer, Training, User
from werkzeug.security import generate_password_hash


def seed_db():
    user_data = [
        {"id": 1, "first_name": "test admin", "last_name": "last_name name", "email": "admin@example.com",
         "role": "admin", "password": generate_password_hash("admin")},
        {"id": 2, "first_name": "test student", "last_name": "last_name name", "email": "student@example.com",
         "role": "student", "password": generate_password_hash("student")},
        {"id": 3, "first_name": "test trainer", "last_name": "last_name name", "email": "trainer@example.com",
         "role": "trainer", "password": generate_password_hash("trainer")},
    ]
    user_instances = seed_table(User, user_data)
    sport_data = [
        {"id": 1, "sport": "test sport"},
    ]
    sport_instances = seed_table(Sport, sport_data)
    trainer_data = [
        {"id": 1, "user_id": 3, "sport_id": 1, "degree": "test degree", "description": "test description"},
    ]
    trainer_instances = seed_table(Trainer, trainer_data)
    subscription_data = [
        {"id": 1, "trainer_id": 1, "sub_name": "test subscription name", "cost": 38, "period": 7},
    ]
    subscription_instance = seed_table(Subscription, subscription_data)
    training_data = [
        {"id": 1, "trainer_id": 1, "description": "test description"},
    ]
    training_instances = seed_table(Training, training_data)

    # insert in SubUser table
    for instance in user_instances:
        if instance.role == 'student':
            instance.subscriptions.append(subscription_instance[0])

    db.session.add_all(
        user_instances + sport_instances + training_instances + trainer_instances + subscription_instance,
    )
    db.session.commit()


def seed_table(table, data):
    instances = list()
    for instance in data:
        instances.append(table(**instance))
    return instances
