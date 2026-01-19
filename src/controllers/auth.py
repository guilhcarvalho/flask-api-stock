from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import create_access_token

from src.app import bcrypt
from src.models import User, db

app = Blueprint("Auth", __name__, url_prefix="/auth_controllers")


def _check_password(pw_hash, password):
    return bcrypt.check_password_hash(pw_hash, password)


@app.route("/login", methods=["POST"])
def _login():
    """Role detail view.
    ---
    post:
      tags:
        - auth
      summary: Auth login
      description: Auth login
      parameters:
        - in: path
          schema: AuthParameter
      responses:
        401:
          description: Unauthorized
    """
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()
    if not user or not _check_password(user.password, password):
        return {"msg": "Bad username or password"}, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=str(user.id))
    return {"access_token": access_token}
