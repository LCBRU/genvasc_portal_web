from celery.schedules import crontab
from sqlalchemy.sql import text
from flask import current_app
from itertools import groupby
from datetime import datetime
from portal.celery import celery
from portal.models import (
    Practice,
    Ccg,
    Federation,
    Delegate,
    User,
    PracticeRegistration,
)
from portal.database import db
from .database import (
    etl_practice_database,
    practice_table,
    ccg_table,
    federation_table,
    delegate_table,
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
        import_practice.s(),
    )


@celery.task
def import_practice():
    current_app.logger.info('Importing practice details')

    practices = []
    practice_registrations = []

    with etl_practice_database() as p_db:
        for p in p_db.execute(practice_table.select()):
            practice = Practice.query.filter_by(
                code=p['practice_code'],
            ).one_or_none()

            if practice is None:
                practice = Practice(
                    code=p['practice_code'],
                )
            
            practice.project_id = p['project_id']
            practice.name = p['practice_name']
            practice.ccg_id = p['ccg']
            practice.street_address = p['practice_address']
            practice.town = p['pract_town']
            practice.city = p['city']
            practice.county = p['county']
            practice.postcode = p['postcode']
            practice.federation = p['federation']
            practice.partners = p['partners']
            practice.genvasc_initiated = p['genvasc_initiated'] == 1
            practice.status = p['status']

            practices.append(practice)

            practice_registration = PracticeRegistration.query.filter_by(
                code=p['practice_code'],
            ).one_or_none()

            if practice_registration is None:
                practice_registrations.append(
                    PracticeRegistration(
                        code=p['practice_code'],
                    )
                )


    db.session.add_all(practices)
    db.session.add_all(practice_registrations)
    db.session.flush()

    updated_practices = Practice.query.with_entities(Practice.code).filter(Practice.id.in_([p.id for p in practices])).subquery()
    PracticeRegistration.query.filter(PracticeRegistration.code.notin_(updated_practices)).delete(synchronize_session='fetch')
    Practice.query.filter(Practice.code.notin_(updated_practices)).delete(synchronize_session='fetch')


@celery.task
def import_ccg():
    current_app.logger.info('Importing ccg details')

    ccgs = []

    with etl_practice_database() as p_db:
        for c in p_db.execute(ccg_table.select()):
            ccg = Ccg.query.filter_by(
                project_id=c['project_id'],
                identifier=c['ccg_id'],
            ).one_or_none()

            if ccg is None:
                ccg = Ccg(
                    project_id=c['project_id'],
                    identifier=c['ccg_id'],
                )
            
            ccg.name = c['name']

            ccgs.append(ccg)

    db.session.add_all(ccgs)
    db.session.flush()
    
    updated_ccgs = Ccg.query.with_entities(Ccg.id).filter(Ccg.id.in_([c.id for c in ccgs])).subquery()
    Ccg.query.filter(Ccg.id.notin_(updated_ccgs)).delete(synchronize_session='fetch')


@celery.task
def import_federation():
    current_app.logger.info('Importing federation details')

    federations = []

    with etl_practice_database() as p_db:
        for f in p_db.execute(federation_table.select()):
            federation = Federation.query.filter_by(
                project_id=f['project_id'],
                identifier=f['federation_id'],
            ).one_or_none()

            if federation is None:
                federation = Federation(
                    project_id=f['project_id'],
                    identifier=f['federation_id'],
                )
            
            federation.name = f['name']

            federations.append(federation)

    db.session.add_all(federations)
    db.session.flush()
    
    updated_federations = Federation.query.with_entities(Federation.id).filter(Federation.id.in_([f.id for f in federations])).subquery()
    Federation.query.filter(Federation.id.notin_(updated_federations)).delete(synchronize_session='fetch')


@celery.task
def import_delegate():
    current_app.logger.info('Importing delegate details')

    delegates = []

    with etl_practice_database() as p_db:
        for f in p_db.execute(delegate_table.select()):
            delegate = Delegate.query.filter_by(
                project_id=f['project_id'],
                practice_code=f['practice_code'],
                instance=f['instance'],
            ).one_or_none()

            if delegate is None:
                delegate = Delegate(
                    project_id=f['project_id'],
                    practice_code=f['practice_code'],
                    instance=f['instance'],
                )
            
            delegate.name = f['name']
            delegate.role = f['role']
            delegate.gcp_trained = f['gcp_trained']
            delegate.gv_trained = f['gv_trained']
            delegate.on_delegation_log_yn = f['on_delegation_log_yn']
            delegate.gv_start_del_log = f['gv_start_del_log']
            delegate.gv_end_del_log = f['gv_end_del_log']
            delegate.gv_phone_a = f['gv_phone_a']
            delegate.gv_phone_b = f['gv_phone_b']
            delegate.contact_email_add = f['contact_email_add']
            delegate.primary_contact_yn = f['primary_contact_yn']

            delegates.append(delegate)

    db.session.add_all(delegates)
    db.session.flush()
    
    updated_delegates = Delegate.query.with_entities(Delegate.id).filter(Delegate.id.in_([f.id for f in delegates])).subquery()
    Delegate.query.filter(Delegate.id.notin_(updated_delegates)).delete(synchronize_session='fetch')


@celery.task
def import_user():
    current_app.logger.info('Importing user details')

    users = []

    with etl_practice_database() as p_db:
        for email, details in groupby(p_db.execute(user_table.select().order_by(user_table.c.email)), key=lambda x: x['email']):
            user = User.query.filter_by(email=email).one_or_none()

            if user is None:
                user = User(email=email)
            
            ds = list(details)

            u = ds[0]
            user.project_id = u['project_id']
            user.current_portal_user_yn = u['current_portal_user_yn']
            user.gv_end_del_log = u['gv_end_del_log']

            user.practices = PracticeRegistration.query.filter(
                PracticeRegistration.code.in_([d['practice_code'] for d in ds])
            ).all()

            users.append(user)

    db.session.add_all(users)
    db.session.flush()
    
    updated = User.query.with_entities(User.id).filter(User.id.in_([u.id for u in users])).subquery()
    User.query.filter(User.id.notin_(updated)).delete(synchronize_session='fetch')
