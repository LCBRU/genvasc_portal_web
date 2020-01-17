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
        "administrator",
        meta,
        Column("id", Integer, primary_key=True),
        Column("email", NVARCHAR(255), index=True, unique=True, nullable=False),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("administrator", meta, autoload=True)
    t.drop()
