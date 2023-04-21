from functools import wraps

from database.models import Roles, User
from flask import abort
from flask_jwt_extended import get_jwt, JWTManager, verify_jwt_in_request


jwt = JWTManager()


def admin_required():
    """decorator for admin access"""

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user = User.query.filter_by(id=claims["sub"]).first()
            if user.role == Roles.admin:
                return fn(*args, **kwargs)
            return abort(403, description="Admins only!")

        return decorator

    return wrapper
