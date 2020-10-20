import json
from datetime import datetime
from unittest import mock
from werkzeug.security import generate_password_hash
from base64 import b64encode
from app import app


class MockPost:
    def __init__(self):
        self.title = 'Post Title'
        self.body = 'Content of post'
        self.date = datetime.strptime('2020-10-01T00:00', '%Y-%m-%dT%H:%M')


class MockUser:
    def __init__(self):
        self.login = 'username'
        self.email = 'username@example.com'
        self.password = generate_password_hash('P@ssw0rd')
        self.uuid = 'uuid'


def get_token():
    credentials = b64encode(b"username:P@ssw0rd").decode('utf-8')

    with mock.patch('app.db.session.query') as query:
        query.return_value.filter_by.return_value.\
            first.return_value = MockUser()

        response = app.test_client().get(
            '/login',
            headers={"Authorization": f"Basic {credentials}"})

    return response.json.get('token')


def test_create_post():
    headers = {'X-Api-Key': get_token()}
    posts_data = dict(title='Post Title', body='Content of post',
                      date='2010-04-01T00:00')

    with mock.patch('app.db.session.add') as add, \
         mock.patch('app.db.session.commit') as commit, \
         mock.patch('app.db.session.query') as query:

        query.return_value.filter_by.return_value.\
            first.return_value = MockUser()

        response = app.test_client().post(
            '/posts',
            data=json.dumps(posts_data),
            headers=headers,
            content_type='application/json')

        add.assert_called_once()
        commit.assert_called_once()

    assert response.status_code == 201
    assert response.json['title'] == 'Post Title'


def test_read_all_post():
    headers = {'X-Api-Key': get_token()}

    with mock.patch('app.db.session.query') as query:
        query.return_value.all.return_value = list()
        query.return_value.filter_by.return_value.\
            first.return_value = MockUser()
        response = app.test_client().get('/posts', headers=headers)

    assert response.status_code == 200
    assert len(response.json) == 0


def test_read_post():
    with mock.patch('app.db.session.query') as query:
        query.return_value.filter_by.return_value.\
            first.return_value = MockPost()
        response = app.test_client().get('/posts/4321')

    assert response.status_code == 200
    assert response.json['title'] == 'Post Title'


def test_update_post():
    with mock.patch('app.db.session.query') as query, \
         mock.patch('app.db.session.add') as add, \
         mock.patch('app.db.session.commit') as commit:

        query.return_value.filter_by.return_value.\
            first.return_value = MockPost()

        response = app.test_client().put(
            '/posts/4321',
            data=json.dumps(dict(title='Post Title (changed)')),
            content_type='application/json'
        )

    assert response.status_code == 200
    assert response.json['title'] == 'Post Title (changed)'


def test_delete_post():
    with mock.patch('app.db.session.query') as query, \
         mock.patch('app.db.session.delete') as delete, \
         mock.patch('app.db.session.commit') as commit:

        query.return_value.filter_by.return_value.\
            first.return_value = MockPost()

        response = app.test_client().delete('/posts/4321')

    assert response.status_code == 204
