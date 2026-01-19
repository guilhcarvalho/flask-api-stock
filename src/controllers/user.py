from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from src.app import bcrypt
from src.models import User, db
from src.services.utils import (InvalidFieldsError, delete_data, requires_role,
                                save_data, update_fields)
from src.views.user import CreateUserSchema, UserSchema

app = Blueprint("user", __name__, url_prefix="/users")


@app.route("/first_user", methods=["POST"])
def _first_user():
    """User detail view.
    ---
    post:
      tags:
        - user
      summary: Create user
      description: Create user
      parameters:
        - in: path
          schema: UserParameter
      responses:
        201:
          description: successful operation
        422:
          description: Unprocessable Entity
        403:
          description: Forbidden
    """
    user_schema = CreateUserSchema()
    
    try:
        data = user_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    
    user = User(username=data["username"],
                password=bcrypt.generate_password_hash(data["password"]),
                role_id=data["role_id"])
    validation = db.session.query(db.session.query(User).exists()).scalar()
    
    if validation == True:
        return {"msg": "The first role already exists."}, HTTPStatus.FORBIDDEN
    
    save_data(user)

    return {"msg": "User created!"}, HTTPStatus.CREATED


@app.route("/get_users/<int:user_id>")
@jwt_required()
@requires_role("admin")
def _get_user(user_id):
    """User detail view.
    ---
    get:
      tags:
        - user
      summary: List user
      description: List user
      parameters:
        - in: path
          name: user_id 
          schema: UserParameter
      responses:
        200:
          description: successful operation
          content:
            aplication/json:
              schema: UserSchema
        404:
          description: Not found user
    """
    user = db.get_or_404(User, user_id)
    user_schema = UserSchema()
    return user_schema.dump(user)


@app.route("/list_users")
@jwt_required()
@requires_role("admin")
def _list_users():
    """Users detail view.
    ---
    get:
      tags:
        - user
      summary: List all users
      description: List all users
      parameters:
          schema: UserParameter
      responses:
        200:
          description: successful operation
          content:
            aplication/json:
              schema: UserSchema
    """
    query = db.select(User)
    users = db.session.execute(query).scalars()
    users_schema = UserSchema(many=True)
    return users_schema.dump(users)


@app.route("/create_users", methods=["POST"])
@jwt_required()
@requires_role("admin")
def _create_user():
    """User detail view.
    ---
    post:
      tags:
        - user
      summary: Create user
      description: Create user
      parameters:
        - in: path
          schema: UserParameter
      responses:
        201:
          description: successful operation
        422:
          description: Unprocessable Entity
    """
    user_schema = CreateUserSchema()
    
    try:
        data = user_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    
    user = User(username=data["username"],
                password=bcrypt.generate_password_hash(data["password"]),
                role_id=data["role_id"])
    
    save_data(user)

    return {"msg": "User created!"}, HTTPStatus.CREATED


@app.route("/update_users/<int:user_id>", methods=["PATCH"])
@jwt_required()
@requires_role("admin")
def _update_user(user_id):
    """User detail view.
    ---
    patch:
      tags:
        - user
      summary: Update user
      description: Update user
      parameters:
        - in: path
          name: user_id 
          schema: UserParameter
      responses:
        200:
          description: successful operation
        404:
          description: Not found user
        400:
          description: Bad request
    """
    user = db.get_or_404(User, user_id)
    data = request.json

    try:
        update_fields(user, data)

    except InvalidFieldsError as e:
        return {
            "error": "Not allowed fields in request",
            "Not allowed fields": list(e.fields),
        }, HTTPStatus.BAD_REQUEST

    return {"msg": "User updated"}, HTTPStatus.OK


@app.route("/delete_users/<int:user_id>", methods=["DELETE"])
@jwt_required()
@requires_role("admin")
def _delete_user(user_id):
    """User detail view.
    ---
    delete:
      tags:
        - user
      summary: Delete user
      description: Delete user
      parameters:
        - in: path
          name: user_id 
          schema: UserParameter
      responses:
        204:
          description: successful operation
        404:
          description: Not found user
    """
    user = db.get_or_404(User, user_id)
    delete_data(user)

    return "", HTTPStatus.NO_CONTENT
