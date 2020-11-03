## Training project that introduces the use of a flask framework for developing web-services.

Source from - https://github.com/denyszamiatin/blog_1

### Technology stack.
    - Flask
    - Flask-Migrate
    - Flask-RESTful
    - Flask-SQLAlchemy
    - poetry (environment manager)
    - Docker, docker-compose
    - nginx
    
    
## Deployment with Docker.
- ### development case:
```bash
docker-compose up -d --build
docker-compose exec web python manage.py db upgrade
```
***.env.dev***
```bash
FLASK_APP=app/__init__.py
DATABASE_URL=postgresql://web_service_user:web_service_password@db:5432/web_service_db
SECRET_KEY='1nqrARb6iP0qFPbA0xAQFUAiBzGHm5OV'
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
```
***.env.dev.db***
```bash
POSTGRES_USER=web_service_user
POSTGRES_PASSWORD=web_service_password
POSTGRES_DB=web_service_db
```

- ### production case:
```bash
docker-compose -f prod.docker-compose.yml up -d --build
docker-compose -f prod.docker-compose.yml exec web python manage.py db upgrade
```
***.env.prod***
```bash
FLASK_APP=app/__init__.py
FLASK_ENV=production
DATABASE_URL=postgresql://web_service_user:web_service_password@db:5432/web_service_db
SECRET_KEY='@#$%^UTYRDsfghj^%'
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
```
***.env.prod.db***
```bash
POSTGRES_USER=web_service_user
POSTGRES_PASSWORD=web_service_password
POSTGRES_DB=web_service_db
```


## Hints.
- *connect to db in container:*
```bash
docker-compose exec db psql --username=web_service_user --dbname=web_service_db
```
- *logs:*
```bash
docker-compose logs -f
```
- *delete all containers (that not running) and images:*
```bash
docker system prune -a
```
- *look at volumes/ inspect volume /delete volumes:*
```bash
docker volumre ls
docker volume inspect <volume>
docker volume rm $(docker volume ls -q)
```


## Deployment without Docker (using local environment).
Install poetry package.
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
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
python manage.py db init
```
Creating migrations.
```bash
python manage.py db migrate
```
Run migrations.
```bash
python manage.py db upgrade
```
Run application.
```bash
python manage.py run
```
## Run tests.
```bash
python -m pytest
```

## curl commands.
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
