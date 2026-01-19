from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from src.models import Role, db
from src.services.utils import requires_role, save_data
from src.views.role import CreateUserSchema

app = Blueprint("role", __name__, url_prefix="/roles")


@app.route("/create_roles", methods=["POST"])
@jwt_required()
@requires_role("admin")
def _create_role():
    """Role detail view.
    ---
    post:
      tags:
        - role
      summary: Create role
      description: Create role
      parameters:
        - in: path
          schema: RoleParameter
      responses:
        201:
          description: successful operation
        422:
          description: Unprocessable Entity
    """
    role_schema = CreateUserSchema()
    
    try:
        data = role_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    
    role = Role(name=data["name"])

    save_data(role)

    return {"msg": "Role created!"}, HTTPStatus.CREATED


@app.route("/first_role", methods=["POST"])
def _first_role():
    """Role detail view.
    ---
    post:
      tags:
        - role
      summary: Create role
      description: Create role
      parameters:
        - in: path
          schema: RoleParameter
      responses:
        201:
          description: successful operation
        422:
          description: Unprocessable Entity
        403:
          description: Forbidden
    """
    role_schema = CreateUserSchema()
    
    try:
        data = role_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    role = Role(name=data["name"])
    validation = db.session.query(db.session.query(Role).exists()).scalar()
    
    if validation == True:
            return {"msg": "The first role already exists."}, HTTPStatus.FORBIDDEN
    
    save_data(role)
    return {"msg": "Role created!"}, HTTPStatus.CREATED
