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
        "role",
        meta,
        Column("id", Integer, primary_key=True),
        Column("name", NVARCHAR(80), index=True, unique=True, nullable=False),
        Column("description", NVARCHAR(255), nullable=False),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("role", meta, autoload=True)
    t.drop()
