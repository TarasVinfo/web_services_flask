from datetime import datetime
from flask import request
from flask_restful import Resource
from . import api, models, db


class PostListApi(Resource):
    def get(self):
        return []

    def post(self):
        request_data = request.json
        post = models.Post(
            title=request_data.get('title'),
            body=request_data.get('body'),
            date=datetime.strptime(request_data.get('date'), '%Y-%m-%dT%H:%M'))
        db.session.add(post)
        db.session.commit()

        return {
                    'title': post.title,
                    'body': post.body,
                    'date': str(post.date),
                    'uuid': post.uuid
                }, 201


class PostApi(Resource):
    def get(self, uuid):
        return ''

    def put(self, uuid):
        return ''

    def delete(self, uuid):
        return '', 204


api.add_resource(PostListApi, '/posts')
api.add_resource(PostApi, '/posts/<uuid>')
