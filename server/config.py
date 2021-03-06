from os import environ
from datetime import timedelta

from dotenv import load_dotenv


load_dotenv('.env')


class BaseConfig:
    HOST = '127.0.0.1'
    PORT = 5000
    USE_PERMANENT_SESSION = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=5)

    CORS_ALLOWED_ORIGINS = ['http//' + HOST + ':' + str(PORT)]

    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=15)

    MAIL_CONFIRM_TOKEN_EXPIRES = timedelta(days=1)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_DEFAULT_SENDER = 'asdsadsa@mail.com'

    task_title_len = 25
    category_name_len = 15
    filename_len = 228
    files_dir_len = 0
    admin_roles = ('admin', 'owner')
    owner_roles = ('owner',)


class DevConfig(BaseConfig):
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)

    SECRET_KEY = environ.get('SECRET_KEY')
    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URL = environ.get('DATABASE_URL')

    AWS_ACCESS_KEY = environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_KEY = environ.get('AWS_SECRET_KEY')
    AWS_BUCKET_NAME = environ.get('AWS_BUCKET_NAME')

    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')

    CELERY_BROKER_URL = environ.get('CELERY_BROKER_URL')
    backend_result = environ.get('CELERY_RESULT_BACKEND')
