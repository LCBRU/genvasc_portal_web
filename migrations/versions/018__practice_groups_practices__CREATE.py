from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    ForeignKey,
)


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    p = Table("etl_practice", meta, autoload=True)
    pg = Table("practice_group", meta, autoload=True)

    t = Table(
        "practice_groups_practices",
        meta,
        Column("practice_group_id", Integer, ForeignKey(p.c.id), index=True, nullable=False),
        Column("practice_id", Integer, ForeignKey(pg.c.id), index=True, nullable=False),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("practice_groups_practices", meta, autoload=True)
    t.drop()
