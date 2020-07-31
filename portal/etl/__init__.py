import random
import string
from celery.schedules import crontab
from sqlalchemy.sql import text
from sqlalchemy.orm import joinedload
from flask import current_app
from itertools import groupby
from datetime import datetime
from portal.celery import celery
from portal.models import (
    Practice,
    PracticeStatus,
    User,
)
from portal.database import db
from portal.utils import parse_date
from .database import (
    etl_practice_database,
    etl_import_database,
    user_table,
    practice_status_table,
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
    sender.add_periodic_task(
        crontab(
            minute=current_app.config['PRACTICE_ETL_SCHEDULE_MINUTE'],
            hour=current_app.config['PRACTICE_ETL_SCHEDULE_HOUR'],
        ),
        import_practice_status.s(),
    )


@celery.task
def import_user():
    current_app.logger.info('Importing user details')

    existing_users = {u.email: u for u in User.query.options(joinedload('practices')).all()}
    practices = {p.code: p for p in Practice.query.all()}

    users = []

    with etl_practice_database() as p_db:
        for email, details in groupby(p_db.execute(user_table.select().order_by(user_table.c.email)), key=lambda x: x['email'].lower()):
            user = existing_users.get(email, None)

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

            user.practices = set([practices[d['practice_code']] for d in ds])

            users.append(user)

    db.session.add_all(users)
    db.session.flush()

    for u in User.query.filter(User.id.notin_([u.id for u in users]), User.is_imported.is_(True)).all():
        db.session.delete(u)

    db.session.commit()


@celery.task
def import_practice_status():
    current_app.logger.info('Importing practice status details')

    practice_statuses = []

    with etl_import_database() as p_db:
        for ps in p_db.execute(practice_status_table.select()):
            practice_status = PracticeStatus.query.filter_by(value=int(ps['id'])).one_or_none()

            if practice_status is None:
                practice_status = PracticeStatus(
                    value=int(ps['id']),
                )
            
            practice_status.name = ps['name']
            
            practice_statuses.append(practice_status)

    db.session.add_all(practice_statuses)
    db.session.flush()
    
    PracticeStatus.query.filter(PracticeStatus.id.notin_([ps.id for ps in practice_statuses])).delete(synchronize_session='fetch')

    db.session.commit()
