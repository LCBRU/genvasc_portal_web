from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    NVARCHAR,
)


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("etl_practice", meta, autoload=True)
    t.c.federation.drop()


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    t = Table("etl_practice", meta, autoload=True)

    ccg_id = Column("federation", NVARCHAR(500), index=True)
    ccg_id.create(t, index_name='idx__practice__federation')
