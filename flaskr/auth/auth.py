from functools import wraps

from flask import jsonify
from flask_jwt_extended import JWTManager, get_jwt, verify_jwt_in_request

jwt = JWTManager()


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_administrator"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403

        return decorator

    return wrapper

