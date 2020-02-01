from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    NVARCHAR,
    Boolean,
    DateTime,
    Date,
    UniqueConstraint,
)


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    t = Table("etl_delegationLog", meta, autoload=True)
    t.drop(migrate_engine)

    meta = MetaData()
    meta.bind = migrate_engine

    t = Table(
        "etl_delegationLog",
        meta,
        Column("id", Integer, primary_key=True),
        Column("practice_code", NVARCHAR(100), index=True, nullable=False),
        Column("instance", Integer, nullable=False, index=True),
        Column("name", NVARCHAR(500), nullable=False),
        Column("role", NVARCHAR(500), nullable=True),
        Column("gcp_trained", Boolean, nullable=True),
        Column("gv_trained", Boolean, nullable=True),
        Column("on_delegation_log_yn", Boolean, nullable=True),
        Column("gv_start_del_log", Date, nullable=True),
        Column("gv_end_del_log", Date, nullable=True),
        Column("rsn_not_on_del_log", NVARCHAR(500), nullable=True),
        Column("gv_phone_a", NVARCHAR(100), nullable=True),
        Column("gv_phone_b", NVARCHAR(100), nullable=True),
        Column("contact_email_add", NVARCHAR(500), nullable=True),
        Column("primary_contact_yn", Boolean, nullable=True),
        Column("last_update_timestamp", DateTime, nullable=False, index=True),
        UniqueConstraint(
            'practice_code',
            'instance',
            name='uix__etl_delegate__practice_code__instance'
        ),
    )
    t.create()


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    t = Table("etl_delegationLog", meta, autoload=True)
    t.drop(migrate_engine)

    meta = MetaData()
    meta.bind = migrate_engine

    t = Table(
        "etl_delegationLog",
        meta,
        Column("practice_code", NVARCHAR(100), index=True, nullable=False, primary_key=True),
        Column("instance", Integer, nullable=False, primary_key=True),
        Column("name", NVARCHAR(500), nullable=False),
        Column("role", NVARCHAR(500), nullable=True),
        Column("gcp_training", Boolean, nullable=True),
        Column("gv_trained", Boolean, nullable=True),
        Column("on_delegation_log_yn", Boolean, nullable=True),
        Column("gv_start_del_log", DateTime, nullable=True),
        Column("gv_end_del_log", DateTime, nullable=True),
        Column("rsn_not_on_del_log", NVARCHAR(500), nullable=True),
        Column("gv_phone_a", NVARCHAR(100), nullable=True),
        Column("gv_phone_b", NVARCHAR(100), nullable=True),
        Column("contact_email_add", NVARCHAR(100), nullable=True),
        Column("primary_contact_yn", Boolean, nullable=True),

    )
    t.create()
