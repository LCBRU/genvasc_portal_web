from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    NVARCHAR,
    DateTime,
)


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    t = Table(
        "practice_registration",
        meta,
        Column("id", Integer, nullable=False, primary_key=True),
        Column("code", NVARCHAR(50), nullable=False, index=True, unique=True),
        Column("date_created", DateTime, nullable=False),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("user", meta, autoload=True)
    t.drop()
