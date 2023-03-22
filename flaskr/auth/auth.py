from functools import wraps

from flask import abort
from flask_jwt_extended import JWTManager, get_jwt, verify_jwt_in_request

from database.models import User, Roles

jwt = JWTManager()


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user = User.query.filter_by(id=claims["sub"]).first()
            if user.role == Roles.admin:
                return fn(*args, **kwargs)
            else:
                return abort(403, description="Admins only!")

        return decorator

    return wrapper
