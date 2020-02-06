from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    ForeignKey,
    NVARCHAR,
)


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    u = Table("user", meta, autoload=True)
    pg = Table("practice_group", meta, autoload=True)

    t = Table(
        "practice_groups_users",
        meta,
        Column("practice_group_type", NVARCHAR(200), ForeignKey(pg.c.type), index=True, nullable=False),
        Column("practice_group_project_id", Integer, ForeignKey(pg.c.project_id), index=True, nullable=False),
        Column("practice_group_identifier", Integer, ForeignKey(pg.c.identifier), index=True, nullable=False),
        Column("user_id", Integer, ForeignKey(u.c.id), index=True, nullable=False),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("practice_groups_users", meta, autoload=True)
    t.drop()
