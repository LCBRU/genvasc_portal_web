from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, Date, DateTime
from contextlib import contextmanager
from flask import current_app

practice_etl_meta = MetaData()
recruit_etl_meta = MetaData()


practice_table = Table(
    'etl_portal_practice', practice_etl_meta,
    Column('project_id', Integer),
    Column('practice_code', String(10)),
    Column('practice_name', String(100)),
    Column('ccg', Integer),
    Column('practice_address', String(500)),
    Column('pract_town', String(100)),
    Column('city', String(100)),
    Column('county', String(100)),
    Column('postcode', String(20)),
    Column('federation', Integer),
    Column('partners', String(100)),
    Column('genvasc_initiated', Integer),
    Column('status', Integer),
    Column('last_update_timestamp', DateTime),
)


ccg_table = Table(
    'etl_portal_ccg', practice_etl_meta,
    Column('project_id', Integer),
    Column('ccg_id', Integer),
    Column('name', String(100)),
)


federation_table = Table(
    'etl_portal_federation', practice_etl_meta,
    Column('project_id', Integer),
    Column('federation_id', Integer),
    Column('name', String(100)),
)


management_area_table = Table(
    'etl_portal_management_area', practice_etl_meta,
    Column('project_id', Integer),
    Column('name', String(100)),
)


delegate_table = Table(
    'etl_portal_delegate', practice_etl_meta,
    Column('practice_code', String(100)),
    Column('instance', Integer),
    Column('name', String(500)),
    Column('role', String(100)),
    Column('gcp_trained', Boolean),
    Column('gv_trained', Boolean),
    Column('on_delegation_log_yn', Boolean),
    Column('gv_start_del_log', Date),
    Column('gv_end_del_log', Date),
    Column('rsn_not_on_del_log', String(500)),
    Column('gv_phone_a', String(100)),
    Column('gv_phone_b', String(100)),
    Column('contact_email_add', String(100)),
    Column('primary_contact_yn', Boolean),
    Column('last_update_timestamp', DateTime),
)


user_table = Table(
    'etl_portal_user', practice_etl_meta,
    Column('project_id', Integer),
    Column('practice_code', String(100)),
    Column('email', String(250)),
    Column('current_portal_user_yn', Integer),
    Column('gv_end_del_log', String(100)),
    Column('last_update_timestamp', DateTime),
)


recruit_table = Table(
    'etl_portal_recruits', recruit_etl_meta,
    Column('processing_id', String(100)),
    Column('status', String(100)),
    Column('nhs_number', String(100)),
    Column('study_id', String(100)),
    Column('practice_code', String(100)),
    Column('first_name', String(100)),
    Column('last_name', String(100)),
    Column('date_of_birth', Date),
    Column('civicrm_contact_id', Integer),
    Column('civicrm_case_id', Integer),
    Column('processed_date', Date),
    Column('recruited_date', Date),
    Column('invoice_year', Integer),
    Column('invoice_quarter', String(10)),
    Column('reimbursed_status', String(10)),
    Column('last_update_timestamp', DateTime),
)


@contextmanager
def etl_practice_database():
    try:
        current_app.logger.info(f'Starting practice database engine')
        engine = create_engine(
            current_app.config['PRACTICE_DATABASE_URI'],
            echo=current_app.config['SQLALCHEMY_ECHO'],
        )
        practice_etl_meta.bind = engine
        yield engine
    finally:
        engine.dispose()
        current_app.logger.info(f'Disposing practice database engine')


@contextmanager
def etl_recruit_database():
    try:
        current_app.logger.info(f'Starting recruit database engine')
        engine = create_engine(
            current_app.config['RECRUIT_DATABASE_URI'],
            echo=current_app.config['SQLALCHEMY_ECHO'],
        )
        recruit_etl_meta.bind = engine
        yield engine
    finally:
        engine.dispose()
        current_app.logger.info(f'Disposing recruit database engine')
