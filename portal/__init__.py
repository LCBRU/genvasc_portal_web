import logging
from flask import Flask
from .config import BaseConfig
from .database import db
from .emailing import init_mail
from .template_filters import init_template_filters
from .standard_views import init_standard_views
from .security import init_security, init_users
from .utils import ReverseProxied
from .ui import blueprint as ui_blueprint
from .celery import init_celery, celery
from .etl import init_etl
from .admin import init_admin

def create_app(config=BaseConfig):
    app = Flask(__name__)
    app.wsgi_app = ReverseProxied(app.wsgi_app)
    app.config.from_object(config)
    app.config.from_pyfile("application.cfg", silent=True)

    with app.app_context():
        app.logger.setLevel(logging.INFO)
        db.init_app(app)
        init_mail(app)
        init_template_filters(app)
        init_standard_views(app)
        init_security(app)
        init_celery(app)
        init_etl(app)
        init_admin(app)

    app.register_blueprint(ui_blueprint)

    return app
