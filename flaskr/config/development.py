import os

from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

DEBUG = True
SQLALCHEMY_ECHO = False
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
SQLALCHEMY_DATABASE_URI = \
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('DB_URI')}/postgres"
BUNDLE_ERRORS = True
JSON_SORT_KEYS = False

CELERY = {
    "broker_url": os.getenv("BROKER_URL"),
    "timezone": "Europe/Kiev",
    "beat_schedule": {
        'subscription_expiration_check_in_midnight': {
            'task': 'subscription_expiration_check',
            'schedule': crontab(hour=0, minute=0),
        },
    },
}

STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
