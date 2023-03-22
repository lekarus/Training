import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = True
SQLALCHEMY_ECHO = False
SECRET_KEY = os.environ["FLASK_SECRET_KEY"]
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
SQLALCHEMY_DATABASE_URI = \
    f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@localhost:5432/postgres"
BUNDLE_ERRORS = True
JSON_SORT_KEYS = False
