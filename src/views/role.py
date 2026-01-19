from marshmallow import fields

from src.app import ma
from src.models.role import Role


class RoleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Role

    id = ma.auto_field()
    name = ma.auto_field()


class RoleParameter(ma.Schema):
    role_id = fields.Int(required=True)


class CreateUserSchema(ma.SQLAlchemySchema):
    name = fields.String(required=True)

