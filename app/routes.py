from flask import request
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from . import api, db, models, schemas, auth


post_schema = schemas.PostSchema()
user_schema = schemas.UserSchema()


class PostListApi(Resource):
    @auth.token_required
    def get(self, user):
        posts = db.session.query(models.Post).all()
        return post_schema.dump(posts, many=True)

    @auth.token_required
    def post(self, user):
        try:
            post = post_schema.load(request.json, session=db.session)

        except ValidationError as error:
            return {'message': str(error)}, 400

        post.author = user
        db.session.add(post)
        db.session.commit()

        return post_schema.dump(post), 201


class PostApi(Resource):
    def get(self, uuid):
        post = db.session.query(models.Post).filter_by(uuid=uuid).first()

        if post is None:
            return '', 404

        return post_schema.dump(post)

    def put(self, uuid):
        post = db.session.query(models.Post).filter_by(uuid=uuid).first()

        if post is None:
            return '', 404

        post = post_schema.load(request.json, instance=post,
                                session=db.session)

        db.session.add(post)
        db.session.commit()

        return post_schema.dump(post)

    def delete(self, uuid):
        post = db.session.query(models.Post).filter_by(uuid=uuid).first()

        if post is None:
            return '', 404

        db.session.delete(post)
        db.session.commit()

        return '', 204


class UserListApi(Resource):

    def post(self):
        try:
            user = user_schema.load(request.json, session=db.session)

        except ValidationError as error:
            return {'message': str(error)}, 400

        try:
            db.session.add(user)
            db.session.commit()

        except IntegrityError:
            return {'message': 'User exists'}, 409

        return user_schema.dump(user), 201


api.add_resource(PostListApi, '/posts')
api.add_resource(PostApi, '/posts/<uuid>')
api.add_resource(UserListApi, '/users')
