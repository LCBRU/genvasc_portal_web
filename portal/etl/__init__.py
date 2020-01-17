from celery.schedules import crontab
from sqlalchemy.sql import text
from flask import current_app
from portal.celery import celery
from portal.models import Practice
from portal.database import db
from .database import (
    etl_practice_database,
    practice_table,
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