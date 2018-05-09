from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from portal.config import BaseConfig
from flask_wtf.csrf import CsrfProtect
from flask_security import Security, SQLAlchemyUserDatastore
import logging
import traceback
from flask_mail import Mail
from portal.utils import ResetPasswordForm, ChangePasswordForm, ReverseProxied


app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)
app.config.from_object(BaseConfig)
CsrfProtect(app)
mail = Mail(app)


if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler(app.config['SMTP_SERVER'],
                               app.config['APPLICATION_EMAIL_ADDRESS'],
                               app.config['ADMIN_EMAIL_ADDRESSES'],
                               app.config['ERROR_EMAIL_SUBJECT'])
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


@app.errorhandler(500)
@app.errorhandler(Exception)
def internal_error(exception):
    print(traceback.format_exc())
    app.logger.error(traceback.format_exc())
    return render_template('500.html'), 500


# Set up database
db = SQLAlchemy(app)

import portal.database
database.init_db()

from portal.models import *

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore,
                    reset_password_form=ResetPasswordForm,
                    change_password_form=ChangePasswordForm)

from portal.views import *
import portal.security
