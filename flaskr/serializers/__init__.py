from functools import wraps

from flask_marshmallow import Marshmallow
from sqlalchemy import Row

from database import db

ma = Marshmallow()


def serializer_decorator(serializer):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            output = fn(*args, **kwargs)
            status_code = 200

            if type(output) == tuple:
                status_code = output[1]
                output = output[0]

            db_types = (db.Model, Row)
            if type(output) == list and all(isinstance(instance, db_types) for instance in output) \
                    or isinstance(output, db_types):
                return serializer.dump(output), status_code
            else:
                return output, status_code

        return decorator

    return wrapper
