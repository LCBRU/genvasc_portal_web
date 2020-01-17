from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    NVARCHAR,
    Date,
)


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    t = Table(
        "etl_recruit_status",
        meta,
        Column("id", NVARCHAR(50), primary_key=True, nullable=False),
        Column("status", NVARCHAR(100), nullable=True),
        Column("nhs_number", NVARCHAR(20), nullable=True),
        Column("study_id", NVARCHAR(100), nullable=True),
        Column("practice_code", NVARCHAR(100), nullable=True),
        Column("first_name", NVARCHAR(100), nullable=True),
        Column("last_name", NVARCHAR(100), nullable=True),
        Column("date_of_birth", Date, nullable=True),
        Column("civicrm_contact_id", Integer, index=True, nullable=True),
        Column("civicrm_case_id", Integer, index=True, nullable=True),
        Column("processed_by", NVARCHAR(500), nullable=True),
        Column("processed_date", Date, nullable=True),
        Column("date_recruited", Date, nullable=True),
        Column("invoice_year", NVARCHAR(50), nullable=True),
        Column("invoice_quarter", NVARCHAR(50), nullable=True),
        Column("reimbursed_status", NVARCHAR(50), nullable=True),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("etl_recruit_status", meta, autoload=True)
    t.drop()
