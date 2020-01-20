from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    NVARCHAR,
    Boolean,
)


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    t = Table("etl_practice", meta, autoload=True)
    t.drop(migrate_engine)

    meta = MetaData()
    meta.bind = migrate_engine

    t = Table(
        "etl_practice",
        meta,
        Column("id", Integer, nullable=False, primary_key=True),
        Column("project_id", Integer, nullable=False, index=True),
        Column("code", NVARCHAR(50), nullable=False, index=True),
        Column("name", NVARCHAR(100), nullable=False),
        Column("ccg_id", Integer, nullable=True, index=True),
        Column("street_address", NVARCHAR(500), nullable=True),
        Column("town", NVARCHAR(100), nullable=True),
        Column("city", NVARCHAR(100), nullable=True),
        Column("county", NVARCHAR(100), nullable=True),
        Column("postcode", NVARCHAR(100), nullable=True),
        Column("genvasc_initiated", Boolean, nullable=False),
        Column("status", Integer, nullable=False),
        Column("federation", Integer, nullable=False, index=True),
        Column("partners", NVARCHAR(500), nullable=True),
    )
    t.create()



def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    t = Table("etl_practice", meta, autoload=True)
    t.drop(migrate_engine)

    meta = MetaData()
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
