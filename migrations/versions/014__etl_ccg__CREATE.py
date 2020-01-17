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
        "etl_ccg",
        meta,
        Column("project_id", Integer, primary_key=True),
        Column("id", Integer, primary_key=True),
        Column("name", NVARCHAR(255), nullable=False),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("etl_ccg", meta, autoload=True)
    t.drop()
