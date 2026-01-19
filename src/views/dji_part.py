from marshmallow import fields

from src.app import ma
from src.models.dji_part import Dji_Part


class DjiPartSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Dji_Part

    id = ma.auto_field()
    dji_part_number = ma.auto_field()
    name = ma.auto_field()
    quantity = ma.auto_field()
    last_update = ma.auto_field()
    author_id = ma.auto_field()
    

class ItemParameter(ma.Schema):
    item_id = fields.Int(required=True)

    
class CreateItemSchema(ma.SQLAlchemySchema):
    dji_part_number = fields.String(required=True)
    name = fields.String(required=True)
    quantity = fields.Integer(required=True, strict=True)
    author_id = fields.Integer(required=True, strict=True)