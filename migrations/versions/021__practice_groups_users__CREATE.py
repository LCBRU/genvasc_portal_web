from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    ForeignKey,
    NVARCHAR,
    UniqueConstraint,
)


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    u = Table("user", meta, autoload=True)

    t = Table(
        "practice_groups_users",
        meta,
        Column("practice_group_type", NVARCHAR(200), index=True, nullable=False),
        Column("practice_group_project_id", Integer, index=True, nullable=False),
        Column("practice_group_identifier", Integer, index=True, nullable=False),
        Column("user_id", Integer, ForeignKey(u.c.id), index=True, nullable=False),
        UniqueConstraint(
            'user_id',
            'practice_group_type',
            'practice_group_project_id',
            'practice_group_identifier',
            name='uix_practice_groups_users__user_id__practice_group'
        ),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("practice_groups_users", meta, autoload=True)
    t.drop()
