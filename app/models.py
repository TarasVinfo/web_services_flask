from . import db
import uuid


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.Text)
    date = db.Column(db.DateTime)
    uuid = db.Column(db.String(36), unique=True)

    def __init__(self, title, body, date):
        self.title = title
        self.body = body
        self.date = date
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f'Post("{self.title}", "{self.date}", "{self.uuid}")'
