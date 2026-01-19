from marshmallow import fields

from src.app import ma
from src.models.user import User
from src.views.role import RoleSchema


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()
    role = ma.Nested(RoleSchema)

class UserParameter(ma.Schema):
    user_id = fields.Int(required=True)
    
 
class AuthParameter(ma.Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    
    
class CreateUserSchema(ma.SQLAlchemySchema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    role_id = fields.Integer(required=True, strict=True)