from functools import wraps
from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity

from src.models import User, db


def requires_role(*roles):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_id = get_jwt_identity()
            user = db.get_or_404(User, user_id)

            if user.role.name not in roles:
                return {"msg": "User don't have access."}, HTTPStatus.FORBIDDEN
            return f(*args, **kwargs)

        return wrapped

    return decorator


class InvalidFieldsError(Exception):
    def __init__(self, fields):
        self.fields = fields


def update_fields(attribute, data: dict):

    ALLOWED_FIELDS = {"dji_part_number", "quantity", "author_id", "name", "username"}

    NOT_ALLOWED_FIELDS = set(data.keys()) - ALLOWED_FIELDS

    if NOT_ALLOWED_FIELDS:
        raise InvalidFieldsError(NOT_ALLOWED_FIELDS)

    for field in ALLOWED_FIELDS:
        if field in data:
            setattr(attribute, field, data[field])

    db.session.commit()


def delete_data(data):
    db.session.delete(data)
    db.session.commit()


def save_data(data):
    db.session.add(data)
    db.session.commit()
