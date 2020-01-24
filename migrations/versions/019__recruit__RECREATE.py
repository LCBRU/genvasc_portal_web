from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    NVARCHAR,
    Date,
    ForeignKey,
    DateTime,
)


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    t = Table("recruit", meta, autoload=True)
    t.drop(migrate_engine)

    meta = MetaData()
    meta.bind = migrate_engine

    pr = Table("practice_registration", meta, autoload=True)

    t = Table(
        "recruit",
        meta,
        Column("id", Integer, primary_key=True),
        Column("practice_id", Integer, ForeignKey(pr.c.id), index=True, nullable=False),
        Column("processing_id", NVARCHAR(100), index=True, nullable=False),
        Column("nhs_number", NVARCHAR(20), index=True, nullable=False),
        Column("date_of_birth", Date, nullable=False),
        Column("date_recruited", Date, nullable=False),
        Column("nhs_number", NVARCHAR(100), nullable=False),
        Column("study_id", NVARCHAR(100), nullable=True),
        Column("first_name", NVARCHAR(100), nullable=True),
        Column("last_name", NVARCHAR(100), nullable=True),
        Column("processed_date", Date, nullable=True),
        Column("invoice_year", NVARCHAR(50), nullable=True),
        Column("invoice_quarter", NVARCHAR(50), nullable=True),
        Column("reimbursed_status", NVARCHAR(50), nullable=True),
        Column("date_created", DateTime, nullable=True),

        Column("civicrm_contact_id", Integer, index=True, nullable=False),
        Column("civicrm_case_id", Integer, index=True, nullable=False),
    )
    t.create()


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    t = Table("recruit", meta, autoload=True)
    t.drop()

    meta = MetaData()
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
