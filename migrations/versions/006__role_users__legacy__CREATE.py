from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    ForeignKey,
)


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    u = Table("user", meta, autoload=True)
    r = Table("role", meta, autoload=True)

    t = Table(
        "roles_users",
        meta,
        Column("user_id", Integer, ForeignKey(u.c.id), index=True, nullable=False),
        Column("role_id", Integer, ForeignKey(r.c.id), index=True, nullable=False),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("roles_users", meta, autoload=True)
    t.drop()
