from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from . import models


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.User
        exclude = 'id',
        load_instance = True


class AuthorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.User
        exclude = 'id', 'password',
        load_instance = True


class PostSchema(SQLAlchemyAutoSchema):
    author = fields.Nested(AuthorSchema)

    class Meta:
        model = models.Post
        exclude = 'id',
        load_instance = True
