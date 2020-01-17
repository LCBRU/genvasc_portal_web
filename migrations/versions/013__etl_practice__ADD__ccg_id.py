from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
)


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    t = Table("etl_practice", meta, autoload=True)

    ccg_id = Column("ccg_id", Integer, index=True)
    ccg_id.create(t, index_name='idx__practice__ccg_id')


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("etl_practice", meta, autoload=True)
    t.c.ccg_id.drop()
