from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, Date, DateTime
from contextlib import contextmanager
from flask import current_app

practice_etl_meta = MetaData()
recruit_etl_meta = MetaData()
import_meta = MetaData()


practice_status_table = Table(
    'etl_practice_status', import_meta,
    Column('id', Integer),
    Column('name', String(255)),
)



practice_table = Table(
    'etl_practice_detail', import_meta,
    Column('project_id', Integer),
    Column('code', String(10)),
    Column('name', String(100)),
    Column('ccg', Integer),
    Column('street_address', String(500)),
    Column('town', String(100)),
    Column('city', String(100)),
    Column('county', String(100)),
    Column('postcode', String(20)),
    Column('federation', Integer),
    Column('partners', String(100)),
    Column('genvasc_initiated', Integer),
    Column('status_id', Integer),
    Column('collab_ag_comp_yn', Boolean),
    Column('collab_ag_signed_date', Date),
    Column('isa_comp_yn', Boolean),
    Column('isa_1_signed_date', Date),
    Column('isa_1_caldicott_guard_end', Date),
    Column('agree_66_comp_yn', Boolean),
    Column('agree_66_signed_date_1', Date),
    Column('agree_66_end_date_2', Date),
)


practice_group_table = Table(
    'etl_practice_group', import_meta,
    Column('project_id', Integer),
    Column('type', String(255)),
    Column('identifier', String(255)),
    Column('name', String(255)),
)


practice_groups_practices_table = Table(
    'etl_practice_groups_practices', import_meta,
    Column('practice_group_type', String(255)),
    Column('practice_group_project_id', Integer),
    Column('practice_group_identifier', Integer),
    Column('practice_code', String(255)),
)


delegate_table = Table(
    'etl_delegate', import_meta,
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
    'etl_recruit', recruit_etl_meta,
    Column('status', String(100)),
    Column('nhs_number', String(100)),
    Column('study_id', String(100)),
    Column('practice_code', String(100)),
    Column('first_name', String(100)),
    Column('last_name', String(100)),
    Column('date_of_birth', Date),
    Column('civicrm_contact_id', Integer),
    Column('civicrm_case_id', Integer),
    Column('processed_by', String(100)),
    Column('processed_date', Date),
    Column('recruited_date', Date),
    Column('invoice_year', Integer),
    Column('invoice_quarter', String(10)),
    Column('reimbursed_status', String(10)),
    Column('exclusion_reason', String(500)),
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
def etl_import_database():
    current_app.logger.info(f'Starting import database engine')
    try:
        engine = create_engine(
            current_app.config['IMPORT_DATABASE_URI'],
            echo=current_app.config['SQLALCHEMY_ECHO'],
        )
        import_meta.bind = engine
        yield engine
    finally:
        engine.dispose()
        current_app.logger.info(f'Disposing import database engine')
