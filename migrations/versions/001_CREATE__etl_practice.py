from sqlalchemy import (
    MetaData,
    Table,
    Column,
    NVARCHAR,
)


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    t = Table(
        "etl_practice",
        meta,
        Column("code", NVARCHAR(50), nullable=False, primary_key=True),
        Column("name", NVARCHAR(100), nullable=False),
        Column("ccg_name", NVARCHAR(500), nullable=True),
        Column("address", NVARCHAR(500), nullable=True),
        Column("federation", NVARCHAR(500), nullable=False, index=True),
        Column("partners", NVARCHAR(500), nullable=True),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("etl_practice", meta, autoload=True)
    t.drop()
