import datetime
import flask_admin as admin
from flask_admin.form import SecureForm
from flask_admin.contrib.sqla import ModelView, fields
from flask_admin.contrib.sqla.view import func
from flask_login import current_user
from .database import db
from .models import (
    User,
    Role,
    PracticeGroup,
)


class QuerySelectMultipleFieldSet(fields.QuerySelectMultipleField):
    def populate_obj(self, obj, name):
        print('*'*500)
        print(name)
        print('*'*500)
        setattr(obj, name, set(self.data))


class CustomView(ModelView):
    # Enable CSRF
    form_base_class = SecureForm

    def is_accessible(self):
        return current_user.is_admin


class UserView(CustomView):
    def get_query(self):
      return self.session.query(self.model).filter(self.model.is_imported==False)

    def get_count_query(self):
      return self.session.query(func.count('*')).filter(self.model.is_imported==False)

    column_exclude_list = [
        'project_id',
        'password',
        'current_login_at',
        'last_login_ip',
        'current_login_ip',
        'login_count',
        'last_update_timestamp',
        'current_portal_user_yn',
        'gv_end_del_log',
        'is_imported',
    ]
    form_columns = [
        "email",
        "first_name",
        "last_name",
        "active",
        "roles",
        "practice_groups",
    ]

    # form_args and form_overrides required to allow roles to be sets.
    form_args = {
        'roles': {
            'query_factory': lambda: db.session.query(Role)
        },
        'practice_groups': {
            'query_factory': lambda: db.session.query(PracticeGroup)
        },
    }
    form_overrides = {
        'roles': QuerySelectMultipleFieldSet,
        'practice_groups': QuerySelectMultipleFieldSet,
    }


def init_admin(app):
    flask_admin = admin.Admin(app, name="GENVASC GP Portal", url="/admin")
    flask_admin.add_view(UserView(User, db.session))
