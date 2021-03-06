from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    NVARCHAR,
    DateTime,
    Boolean,
)


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    t = Table(
        "user",
        meta,
        Column("id", Integer, primary_key=True),
        Column("email", NVARCHAR(255), index=True, unique=True, nullable=False),
        Column("password", NVARCHAR(255), nullable=False),
        Column("first_name", NVARCHAR(255)),
        Column("last_name", NVARCHAR(255)),
        Column("active", Boolean),
        Column("confirmed_at", DateTime),
        Column("last_login_at", DateTime),
        Column("current_login_at", DateTime),
        Column("last_login_ip", NVARCHAR(50)),
        Column("current_login_ip", NVARCHAR(50)),
        Column("login_count", Integer),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("user", meta, autoload=True)
    t.drop()
