from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    ForeignKey,
    UniqueConstraint,
)


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    u = Table("user", meta, autoload=True)
    pr = Table("practice_registration", meta, autoload=True)

    t = Table(
        "practice_registrations_users",
        meta,
        Column("user_id", Integer, ForeignKey(u.c.id), index=True, nullable=False),
        Column("practice_registration_id", Integer, ForeignKey(pr.c.id), index=True, nullable=False),
        UniqueConstraint(
            'user_id',
            'practice_registration_id',
            name='uix_pru__user_id__practice_registration_id'
        ),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("practice_registrations_users", meta, autoload=True)
    t.drop()
