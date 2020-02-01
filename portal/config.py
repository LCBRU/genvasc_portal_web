import os

from dotenv import load_dotenv

# Load environment variables from '.env' file.
load_dotenv()


class BaseConfig(object):
    MAIL_SERVER = os.environ['MAIL_SERVER']
    SECURITY_EMAIL_SENDER = os.environ['LCBRUIT_EMAIL_ADDRESS']

    SECRET_KEY = os.environ['GGPP_FLASK_SECRET_KEY']
    DEBUG = os.environ['GGPP_FLASK_DEBUG'] == 'True'
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = (
        os.environ['GGPP_SQLALCHEMY_TRACK_MODIFICATIONS'] == 'True'
    )
    SQLALCHEMY_ECHO = os.environ['GGPP_SQLALCHEMY_ECHO'] == 'True'
    SECURITY_PASSWORD_HASH = os.environ['GGPP_SECURITY_PASSWORD_HASH']
    SECURITY_PASSWORD_SALT = os.environ['GGPP_SECURITY_PASSWORD_SALT']
    SECURITY_TRACKABLE = os.environ['GGPP_SECURITY_TRACKABLE'] == 'True'
    SMTP_SERVER = 'localhost'
    APPLICATION_EMAIL_ADDRESS = os.environ['LCBRUIT_EMAIL_ADDRESS']
    ERROR_EMAIL_SUBJECT = 'GENVASC Portal Error'
    SECURITY_CHANGEABLE = True
    SECURITY_RECOVERABLE = True
    MAIL_DEFAULT_SENDER = os.environ["LCBRUIT_EMAIL_ADDRESS"]

    # Admin user
    ADMIN_EMAIL_ADDRESS = os.environ['ADMIN_EMAIL_ADDRESS']
    ADMIN_FIRST_NAME = os.environ['ADMIN_FIRST_NAME']
    ADMIN_LAST_NAME = os.environ['ADMIN_LAST_NAME']
    ADMIN_PASSWORD = os.environ['ADMIN_PASSWORD']

    # Celery Settings
    broker_url=os.environ["BROKER_URL"]
    result_backend=os.environ["CELERY_RESULT_BACKEND"]
    CELERY_RATE_LIMIT=os.environ["CELERY_RATE_LIMIT"]
    CELERY_REDIRECT_STDOUTS_LEVEL=os.environ["CELERY_REDIRECT_STDOUTS_LEVEL"]
    CELERY_DEFAULT_QUEUE=os.environ["CELERY_DEFAULT_QUEUE"]

    # Celery Schedules
    PRACTICE_ETL_SCHEDULE_MINUTE=os.environ["PRACTICE_ETL_SCHEDULE_MINUTE"]
    PRACTICE_ETL_SCHEDULE_HOUR=os.environ["PRACTICE_ETL_SCHEDULE_HOUR"]

    # Databases
    PRACTICE_DATABASE_URI=os.environ["PRACTICE_DATABASE_URI"]
    RECRUIT_DATABASE_URI=os.environ["RECRUIT_DATABASE_URI"]
    IMPORT_DATABASE_URI=os.environ["IMPORT_DATABASE_URI"]


class TestConfig(BaseConfig):
    """Configuration for automated testing"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI="sqlite://"
    PRACTICE_DATABASE_URI="sqlite://"
    RECRUIT_DATABASE_URI="sqlite://"
    WTF_CSRF_ENABLED = False
    SMTP_SERVER = None
    SQLALCHEMY_ECHO = False
    broker_url=os.environ["BROKER_URL"] + '/test'


class TestConfigCRSF(TestConfig):
    WTF_CSRF_ENABLED = True
