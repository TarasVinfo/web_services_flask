import pathlib
import os

BASE_DIR = pathlib.Path(__file__).parent


class Config:
    # TODO: refactor env names to file.
    DEBUG = True
    FLASK_ENV = 'development'
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///' + str(BASE_DIR / 'db.sqlite3'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '@#$%^UTYRDsfghj^%'


class ProductionConfig(Config):
    DEBUG = False
