from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    NVARCHAR,
    Date,
    ForeignKey,
)


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    pr = Table("practice_registration", meta, autoload=True)
    u = Table("user", meta, autoload=True)

    t = Table(
        "recruit",
        meta,
        Column("id", Integer, primary_key=True),
        Column("practice_registration_id", Integer, ForeignKey(pr.c.id), index=True, nullable=False),
        Column("user_id", Integer, ForeignKey(u.c.id), index=True, nullable=False),
        Column("nhs_number", NVARCHAR(20), index=True, nullable=False),
        Column("date_of_birth", Date, nullable=False),
        Column("date_recruited", Date, nullable=False),
        Column("civicrm_contact_id", Integer, index=True, nullable=False),
        Column("civicrm_case_id", Integer, index=True, nullable=False),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("recruit", meta, autoload=True)
    t.drop()
