from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from src.models import Dji_Part, db
from src.services.utils import (InvalidFieldsError, delete_data, requires_role,
                                save_data, update_fields)
from src.views.dji_part import CreateItemSchema, DjiPartSchema

app = Blueprint("dji_part", __name__, url_prefix="/dji_parts")


@app.route("/get_itens/<int:item_id>")
@jwt_required()
@requires_role("admin", "client")
def _get_item(item_id):
    """Item detail view.
    ---
    get:
      tags:
        - dji part
      summary: List item
      description: List item
      parameters:
        - in: path
          name: item_id 
          schema: ItemParameter
      responses:
        200:
          description: successful operation
          content:
            aplication/json:
              schema: DjiPartSchema
        404:
          description: Not found user
    """
    item = db.get_or_404(Dji_Part, item_id)
    item_schema = DjiPartSchema()
    return item_schema.dump(item)


@app.route("/register_item", methods=["POST"])
@jwt_required()
@requires_role("admin")
def _register_item():
    """Item detail view.
    ---
    post:
      tags:
        - dji part
      summary: Register item
      description: Register item
      parameters:
        - in: path
          schema: ItemParameter
      responses:
        201:
          description: successful operation
          content:
            aplication/json:
              schema: DjiPartSchema
        422:
          description: Unprocessable Entity
    """
    item_schema = CreateItemSchema()
    
    try:
        data = item_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    
    
    register_item = Dji_Part(
        dji_part_number=data["dji_part_number"],
        name=data["name"],
        quantity=data["quantity"],
        author_id=data["author_id"],
    )

    save_data(register_item)

    return {"msg": "Registered item!"}, HTTPStatus.CREATED


@app.route("/list_itens")
@jwt_required()
@requires_role("admin", "client")
def _list_itens():
    """Item detail view.
    ---
    get:
      tags:
        - dji part
      summary: List itens
      description: List itens
      parameters:
        - in: path
          schema: ItemParameter
      responses:
        200:
          description: successful operation
          content:
            aplication/json:
              schema: DjiPartSchema
    """
    query = db.select(Dji_Part)
    itens = db.session.execute(query).scalars()
    djipart_schema = DjiPartSchema(many=True) 
    return djipart_schema.dump(itens)
    

@app.route("/update_itens/<int:item_id>", methods=["PATCH"])
@jwt_required()
@requires_role("admin")
def _update_item(item_id):
    """Item detail view.
    ---
    patch:
      tags:
        - dji part
      summary: Update item
      description: Update item
      parameters:
        - in: path
          name: item_id
          schema: ItemParameter
      responses:
        200:
          description: successful operation
        400:
          description: Bad request      
        404:
          description: Not found item
    """
    item = db.get_or_404(Dji_Part, item_id)
    data = request.json

    try:
        update_fields(item, data)

    except InvalidFieldsError as e:
        return {
            "error": "Not allowed fields in request",
            "Not allowed fields": list(e.fields),
        }, HTTPStatus.BAD_REQUEST

    return {"msg": "Item updated"}, HTTPStatus.OK


@app.route("/delete_itens/<int:item_id>", methods=["DELETE"])
@jwt_required()
@requires_role("admin")
def _delete_item(item_id):
    """Item detail view.
    ---
    delete:
      tags:
        - dji part
      summary: Delete item
      description: Delete item
      parameters:
        - in: path
          name: item_id
          schema: ItemParameter
      responses:
        200:
          description: successful operation
        404:
          description: Not found item
    """
    item = db.get_or_404(Dji_Part, item_id)
    delete_data(item)

    return "", HTTPStatus.NO_CONTENT
