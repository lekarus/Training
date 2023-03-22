def create_app(config="config.development"):
    from flask import Flask

    from auth.auth import jwt
    from database import db, migrate
    from serializers import ma

    app = Flask(__name__)
    app.config.from_object(config)

    with app.app_context():
        register_blueprints(app)

        jwt.init_app(app)
        db.init_app(app)
        migrate.init_app(app, db)
        ma.init_app(app)

        print(list(app.blueprints.keys())) # noqa T201

    return app


def register_blueprints(app):
    from blueprints.crud import crud
    from blueprints.auth import auth

    app.register_blueprint(crud)
    app.register_blueprint(auth)


if __name__ == '__main__':
    flask_app = create_app()
    with flask_app.app_context():
        flask_app.run()
