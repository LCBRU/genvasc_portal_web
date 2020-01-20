from celery.schedules import crontab
from sqlalchemy.sql import text
from flask import current_app
from portal.celery import celery
from portal.models import Practice, Ccg, Federation
from portal.database import db
from .database import (
    etl_practice_database,
    practice_table,
    ccg_table,
    federation_table,
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

    db.session.add_all(practices)
    db.session.flush()

    updated_practices = Practice.query.with_entities(Practice.id).filter(Practice.id.in_([p.id for p in practices])).subquery()
    Practice.query.filter(Practice.id.notin_(updated_practices)).delete(synchronize_session='fetch')


@celery.task
def import_ccg():
    current_app.logger.info('Importing ccg details')

    ccgs = []

    with etl_practice_database() as p_db:
        for c in p_db.execute(ccg_table.select()):
            ccg = Ccg.query.filter_by(
                project_id=c['project_id'],
                ccg_id=c['ccg_id'],
            ).one_or_none()

            if ccg is None:
                ccg = Ccg(
                    project_id=c['project_id'],
                    ccg_id=c['ccg_id'],
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
                federation_id=f['federation_id'],
            ).one_or_none()

            if federation is None:
                federation = Federation(
                    project_id=f['project_id'],
                    federation_id=f['federation_id'],
                )
            
            federation.name = f['name']

            federations.append(federation)

    db.session.add_all(federations)
    db.session.flush()
    
    updated_federations = Federation.query.with_entities(Federation.id).filter(Federation.id.in_([f.id for f in federations])).subquery()
    Federation.query.filter(Federation.id.notin_(updated_federations)).delete(synchronize_session='fetch')
