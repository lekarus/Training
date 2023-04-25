from flask import Flask
from services.celery import celery_init_app
import stripe


def create_app(config="config.development"):

    from auth.auth import jwt
    from database import db, migrate
    from serializers import ma

    app = Flask(__name__)
    app.config.from_object(config)
    stripe.api_key = app.config["STRIPE_API_KEY"]

    with app.app_context():
        register_blueprints(app)

        jwt.init_app(app)
        db.init_app(app)
        migrate.init_app(app, db)
        ma.init_app(app)
        app.config.from_prefixed_env()
        celery_init_app(app)
        print(list(app.blueprints.keys()))  # noqa T201

    return app


def register_blueprints(app: Flask):
    from blueprints.crud import crud
    from blueprints.auth import auth
    from blueprints.subscriptions import subscriptions
    from blueprints.notification import notification

    app.register_blueprint(crud)
    app.register_blueprint(subscriptions)
    app.register_blueprint(auth)
    app.register_blueprint(notification)


if __name__ == '__main__':
    flask_app = create_app()
    with flask_app.app_context():
        flask_app.run(host="0.0.0.0")
