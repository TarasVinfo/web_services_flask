import datetime
from flask import request, jsonify
from werkzeug.security import check_password_hash
import jwt
from . import app, db, models


@app.route('/login')
def login():
    auth = request.authorization
    message = {"WWW-Authenticate": 'Basic realm="Authentication required"'}

    if not auth:
        return '', 401, message

    username = auth.get('username', '')
    user = db.session.query(models.User).filter_by(login=username).first()
    check_password = check_password_hash(
        user.password, auth.get("password", ""))

    if user is None or not check_password:
        return '', 404, message

    token = jwt.encode({
        "user_id": user.uuid,
        "exp": datetime.datetime.now() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'])

    return jsonify({'token': token.decode('utf-8')})


def token_required(func):
    def wrapper(self, *args, **kwargs):
        token = request.headers.get('X-Api-Key', '')
        message = {"WWW-Authenticate": 'Basic realm="Authentication required"'}

        if not token:
            return '', 401, message

        try:
            uuid = jwt.decode(token, app.config['SECRET_KEY'])['user_id']

        except (KeyError, jwt.ExpiredSignatureError):
            return '', 401, message

        user = db.session.query(models.User).filter_by(uuid=uuid).first()

        if not user:
            return '', 401, message

        return func(self, user, *args, **kwargs)

    return wrapper
