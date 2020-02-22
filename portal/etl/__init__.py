import random
import string
from celery.schedules import crontab
from sqlalchemy.sql import text
from flask import current_app
from itertools import groupby
from datetime import datetime
from portal.celery import celery
from portal.models import (
    Practice,
    User,
)
from portal.database import db
from portal.utils import parse_date
from .database import (
    etl_practice_database,
    user_table,
)


def init_etl(app):
    pass


@celery.on_after_configure.connect
def setup_import_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(
            minute=current_app.config['PRACTICE_ETL_SCHEDULE_MINUTE'],
            hour=current_app.config['PRACTICE_ETL_SCHEDULE_HOUR'],
        ),
        import_user.s(),
    )


@celery.task
def import_user():
    current_app.logger.info('Importing user details')

    users = []

    with etl_practice_database() as p_db:
        for email, details in groupby(p_db.execute(user_table.select().order_by(user_table.c.email)), key=lambda x: x['email'].lower()):
            user = User.query.filter_by(email=email).one_or_none()

            if user is None:
                user = User(email=email)
            
            ds = list(details)

            u = ds[0]
            user.project_id = u['project_id']
            user.current_portal_user_yn = bool(u['current_portal_user_yn'])
            user.gv_end_del_log = parse_date(u['gv_end_del_log'])
            user.last_update_timestamp = u['last_update_timestamp']
            user.is_imported = True
            user.active = bool(u['current_portal_user_yn'])

            user.practices = set(Practice.query.filter(
                Practice.code.in_([d['practice_code'] for d in ds])
            ).all())

            users.append(user)

    db.session.add_all(users)
    db.session.flush()
    
    User.query.filter(User.id.notin_([u.id for u in users]), User.is_imported.is_(True)).delete(synchronize_session='fetch')

    db.session.commit()
