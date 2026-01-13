from functools import wraps
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity
from src.models.models import User, db


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