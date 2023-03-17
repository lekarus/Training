import os

DEBUG = False
SQLALCHEMY_ECHO = False
SECRET_KEY = "my secret key"
SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:5432/postgres"
BUNDLE_ERRORS = True
