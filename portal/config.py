import os


class BaseConfig(object):
    MAIL_SERVER = os.environ['MAIL_SERVER']
    SECURITY_EMAIL_SENDER = os.environ['LCBRUIT_EMAIL_ADDRESS']

    SECRET_KEY = os.environ['GGPP_FLASK_SECRET_KEY']
    DEBUG = os.environ['GGPP_FLASK_DEBUG'] == 'True'
    DB_HOST = os.environ['GGPP_DB_HOST']
    DB_NAME = os.environ['GGPP_DB_NAME']
    DB_USER = os.environ['GGPP_DB_USER']
    DB_PASS = os.environ['GGPP_DB_PASSWORD']
    SQLALCHEMY_DATABASE_URI = 'mysql://{0}:{1}@{2}/{3}'.format(
        DB_USER, DB_PASS, DB_HOST, DB_NAME
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = (
        os.environ['GGPP_SQLALCHEMY_TRACK_MODIFICATIONS'] == 'True'
    )
    SQLALCHEMY_ECHO = os.environ['GGPP_SQLALCHEMY_ECHO'] == 'True'
    SECURITY_PASSWORD_HASH = os.environ['GGPP_SECURITY_PASSWORD_HASH']
    SECURITY_PASSWORD_SALT = os.environ['GGPP_SECURITY_PASSWORD_SALT']
    SECURITY_TRACKABLE = os.environ['GGPP_SECURITY_TRACKABLE'] == 'True'
    SMTP_SERVER = 'localhost'
    APPLICATION_EMAIL_ADDRESS = os.environ['LCBRUIT_EMAIL_ADDRESS']
    ADMIN_EMAIL_ADDRESSES = os.environ['ADMIN_EMAIL_ADDRESS']
    ERROR_EMAIL_SUBJECT = 'GENVASC Portal Error'
    SECURITY_CHANGEABLE = True
    SECURITY_RECOVERABLE = True
