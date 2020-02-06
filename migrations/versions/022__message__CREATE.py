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
        "message",
        meta,
        Column("id", Integer, primary_key=True),
        Column("category", NVARCHAR(100), nullable=False),
        Column("message", NVARCHAR(500), nullable=False),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("message", meta, autoload=True)
    t.drop()
