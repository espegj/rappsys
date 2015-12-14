import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'my_precious'
DEBUG = True
BCRYPT_LOG_ROUNDS = 13
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')