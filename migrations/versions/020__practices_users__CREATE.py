from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    ForeignKey,
    UniqueConstraint,
    NVARCHAR,
)


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    u = Table("user", meta, autoload=True)

    t = Table(
        "practices_users",
        meta,
        Column("user_id", Integer, ForeignKey(u.c.id), index=True, nullable=False),
        Column("practice_code", NVARCHAR(100), index=True, nullable=False),
        UniqueConstraint(
            'user_id',
            'practice_code',
            name='uix_practices_users__user_id__practice_code'
        ),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("practices_users", meta, autoload=True)
    t.drop()
