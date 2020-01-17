from celery.schedules import crontab
from sqlalchemy.sql import text
from flask import current_app
from portal.celery import celery
from portal.models import Practice, Ccg
from portal.database import db
from .database import (
    etl_practice_database,
    practice_table,
    ccg_table,
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
            practices.append(
                Practice(
                    code=p['practice_code'],
                    name=p['practice_name'],
                    ccg_id=p['ccg'],
                    address=p['practice_address'],
                    partners=p['partners'],
                )
            )

    db.session.add_all(practices)


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
