import string
from flask import g, current_app
from flask_login import LoginManager, current_user
from flask_security import Security, SQLAlchemyUserDatastore
from sqlalchemy.orm import joinedload
from wtforms import PasswordField, SubmitField
from flask_security.forms import (
    EqualTo,
    password_required,
    get_form_field_label,
    ValidatorMixin,
    Form,
    PasswordFormMixin,
)
from wtforms.validators import ValidationError
from flask_security.utils import verify_and_update_password, get_message
from .models import User, Role
from .database import db


SYSTEM_USER_EMAIL = 'system@genvasc.nhs.uk'


class PasswordPolicy(ValidatorMixin):
    def __init__(self, message=u'The password must contain a lowercase, '
                 'uppercase and punctuation character'):
        self.message = message

    def __call__(self, form, field):
        value = set(field.data)

        if (value.isdisjoint(string.ascii_lowercase) or
           value.isdisjoint(string.ascii_uppercase) or
           value.isdisjoint(string.punctuation)):
            raise ValidationError(self.message)


class NewPasswordFormMixin():
    password = PasswordField(
        get_form_field_label('password'),
        validators=[password_required, password_length, PasswordPolicy()])


class PasswordConfirmFormMixin():
    password_confirm = PasswordField(
        get_form_field_label('retype_password'),
        validators=[EqualTo('password', message='RETYPE_PASSWORD_MISMATCH'),
                    password_required])


class ResetPasswordForm(Form, NewPasswordFormMixin, PasswordConfirmFormMixin):
    """The default reset password form"""

    submit = SubmitField(get_form_field_label('reset_password'))


class ChangePasswordForm(Form, PasswordFormMixin):
    """The default change password form"""

    new_password = PasswordField(
        get_form_field_label('new_password'),
        validators=[password_required, PasswordPolicy()])

    new_password_confirm = PasswordField(
        get_form_field_label('retype_password'),
        validators=[EqualTo('new_password',
                            message='RETYPE_PASSWORD_MISMATCH'),
                    password_required])

    submit = SubmitField(get_form_field_label('change_password'))

    def validate(self):
        if not super(ChangePasswordForm, self).validate():
            return False

        if not verify_and_update_password(self.password.data, current_user):
            self.password.errors.append(get_message('INVALID_PASSWORD')[0])
            return False
        if self.password.data.strip() == self.new_password.data.strip():
            self.password.errors.append(get_message('PASSWORD_IS_THE_SAME')[0])
            return False
        return True


def load_user(email):
    return User.query.options(joinedload('roles')).filter_by(email=email).one_or_none()

def init_security(app):
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(
        app,
        user_datastore,
        reset_password_form=ResetPasswordForm,
        change_password_form=ChangePasswordForm,

    )

    security.login_manager.user_loader(load_user)

    @app.before_request
    def get_current_user():
        g.user = current_user


def init_users():
    admin_role = Role.query.filter_by(name=Role.ADMIN_ROLENAME).one_or_none()

    if admin_role is None:
        db.session.add(
            Role(
                name=Role.ADMIN_ROLENAME,
                description=Role.ADMIN_ROLENAME,
            )
        )

    admin_user = User.query.filter_by(email=current_app.config["ADMIN_EMAIL_ADDRESS"]).one_or_none()

    if admin_user is None:
        u = User(
            email=current_app.config["ADMIN_EMAIL_ADDRESS"],
            password=current_app.config["ADMIN_PASSWORD"],
            first_name=current_app.config["ADMIN_FIRST_NAME"],
            last_name=current_app.config["ADMIN_LAST_NAME"],
            active=True,
        )
        db.session.add(u)
        u.roles.add(Role.query.filter_by(name=Role.ADMIN_ROLENAME).one_or_none())

        db.session.commit()
