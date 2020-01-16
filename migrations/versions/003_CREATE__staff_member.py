from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    NVARCHAR,
    DateTime,
    ForeignKey,
)


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    pr = Table("practice_registration", meta, autoload=True)

    t = Table(
        "staff_member",
        meta,
        Column("id", Integer, primary_key=True),
        Column("practice_registration_id", Integer, ForeignKey(pr.c.id), index=True, nullable=False),
        Column("first_name", NVARCHAR(50), nullable=False),
        Column("last_name", NVARCHAR(50), nullable=False),
        Column("date_created", DateTime, nullable=False),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("staff_member", meta, autoload=True)
    t.drop()
