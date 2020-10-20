## Training project that introduces the use of a flask framework for developing web-services.

Source from - https://github.com/denyszamiatin/blog_1

### Technology stack.
    - Flask
    - Flask-Migrate
    - Flask-RESTful
    - Flask-SQLAlchemy

### Start project.
Install dependencies.
```bash
poetry install
```
Activate virtual environment.
```bash
poetry shell
```
Initialize migration repository, runs at once.
```bash
flask db init
```
Creating migrations.
```bash
flask db migrate
```
Run migrations.
```bash
flask db upgrade
```
Run application.
```bash
flask run
```
### Run tests.
```bash
python -m pytest
```

### curl commands.
create user:
```bash
curl -X POST http://localhost:5000/users -v -H "Content-type: application/json" -d '{"login": "username", "email": "username@example.com", "password": "P@ssw0rd"}'
```
login and obtain token:
```bash
curl http://localhost:5000/login --user username:P@ssw0rd -v
```
get all posts:
```bash
curl http://localhost:5000/posts -v -H "X-Api-Key: <obtained.token.after_login>"
```
create post:
```bash
curl -X POST http://localhost:5000/posts -v -H "X-Api-Key: <obtained.token.after_login>" -H "Content-type: application/json" -d '{"title": "Title Post", "body": "This post created for testing app", "date": "2020-10-01T00:00"}'
```
get post:
```bash
curl http://localhost:5000/posts/<uuid> -v
```
update post:
```bash
curl -X PUT http://localhost:5000/posts/<uuid> -H "Content-type: application/json" -d '{"title": "Title Post (changed)"}' -v
```