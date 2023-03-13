from flask import current_app
from flask_sqlalchemy import SQLAlchemy
import os

app = current_app
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgres://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:5432/postgres"
db = SQLAlchemy(app)
