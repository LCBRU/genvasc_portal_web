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

    t = Table(
        "practice_status",
        meta,
        Column("id", Integer, primary_key=True),
        Column("value", Integer, index=True),
        Column("name", NVARCHAR(500), nullable=False),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("practice_status", meta, autoload=True)
    t.drop()
