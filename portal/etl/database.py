from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean
from contextlib import contextmanager
from flask import current_app

meta = MetaData()


practice_table = Table(
    'etl_portal_practice', meta,
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
)


ccg_table = Table(
    'etl_ccg', meta,
    Column('project_id', Integer),
    Column('ccg_id', Integer),
    Column('name', String(100)),
)


@contextmanager
def etl_practice_database():
    try:
        current_app.logger.info(f'Starting practice database engine')
        engine = create_engine(
            current_app.config['PRACTICE_DATABASE_URI'],
            echo=current_app.config['SQLALCHEMY_ECHO'],
        )
        meta.bind = engine
        yield engine
    finally:
        engine.dispose()
        current_app.logger.info(f'Disposing practice database engine')
